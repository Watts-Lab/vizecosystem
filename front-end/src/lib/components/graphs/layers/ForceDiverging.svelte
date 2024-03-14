<script lang='ts'>
    // import node_modules
    import { getContext, createEventDispatcher } from 'svelte';
    import { geoAlbersUsa } from 'd3-geo'
    import { forceSimulation, forceCollide, forceManyBody } from 'd3-force';
    import { path } from 'd3-path'
    
    // import components
    import MapAnnotation from '$lib/components/graphs/tooltips/MapAnnotation.svelte';
    import ClickCta from '$lib/components/graphs/layers/ClickCTA.svelte';

    // import utils
    import { formatPct, formatThousands2SI } from '$lib/utils/format-numbers'
    
    const { height, width, rScale, zScale, data } = getContext('LayerCake');

    const percent = formatPct(1);
    
    // variable declaration
    export let collideStrength: number = 1;
    export let manyBodyStrength: number = 1;
    export let medium: string;
    export let diet_threshold: number;
    export let partisanship_scenario: string;
    export let renderAnnotation: boolean;
    export let userHasInteracted: boolean;
    export let userTakingTooLong: boolean;
    export let renderCta: boolean;

    // instantiate event dispatcher
    const dispatch = createEventDispatcher();

    // instantiate projection
    const projection = geoAlbersUsa()
      projection.translate([ $width / 2, $height / 2 ]);

    function restart() {
      simulation.alpha(1).restart();
    }

    // variable declaration
    let rRatio = 9.5;
    let simulationStopped = false;
    let nodes = []
    let simulation = forceSimulation()
      .alpha(0)
      .alphaMin(0.4)
      .force(
        'collide', 
        forceCollide(d => d.r + rRatio)
          .strength(collideStrength)
          .iterations(5)
      )
      .force('charge', forceManyBody().strength(manyBodyStrength))

    function parseNodes(arr) {
      return arr.map((d, i) => {
        const [ x, y ] = projection(d.coordinates)
        const r_L = $rScale(Math.abs(d.data.left_size))
        const r_R = $rScale(Math.abs(d.data.right_size))

        const rightPathString = arcGen(path(), { r: r_R, start: -Math.PI/2, end: Math.PI/2 })
        const fillR = $zScale(d.data.right_pct * 1)

        const leftPathString = arcGen(path(), { r: r_L, start: Math.PI/2, end: -Math.PI/2 })
        const fillL = $zScale(d.data.left_pct * -1)

        const fullPath = pathGen(path(), { r: r_R }, { r: r_L })

        return ({ ...d, 
          x, 
          y,
          r: Math.max(r_L, r_R),
          r_L,
          r_R,
          rightPathString,
          fillR,
          leftPathString,
          fillL,
          fullPath,
        })
      }
    )}

    $: nodes = parseNodes($data)
    
    $: simulation = simulation
      .nodes(nodes)
      .on("tick", () => {
        nodes = simulation.nodes();
      })
      .on('end', () => {
        simulationStopped = true;
        labelActive = true;
      });

    $: {
      { medium, diet_threshold, partisanship_scenario }
      restart()
    }

    $: {
      projection.translate([ $width / 2, $height / 2 ])
      nodes = nodes = parseNodes($data)
      restart()
    }

    $: labelActive = false;
    $: activeState = false;
    $: hoverState = false;

    function handleClick(e: Event, d: any) {
      dispatch('click', { target: e.target, node: d })
    }

    function handleMouseEnter(e: Event, node: any) {
      activeState = node.abbr; 
      hoverState = true; 
      userHasInteracted = true; 
      userTakingTooLong = false;
    }

    function handleMouseOut(e: Event) {
      activeState = false; 
      hoverState = false;
    }
    
    function arcGen(
      context: Function, 
      pos: { x: number, y: number }
    ) {
      context.arc(0, 0, pos.r, pos.start, pos.end)
      context.closePath()
      return context;
    }

    function pathGen(
      context: Function, 
      pos1: { x: number, y: number }, 
      pos2: { x: number, y: number }
    ) {
      context.arc(0, 0, pos1.r, -Math.PI/2, Math.PI/2)
      context.arc(0, 0, pos2.r, Math.PI/2, -Math.PI/2)
      context.closePath()
      return context
    }
</script>

{#if renderAnnotation}
  <MapAnnotation data={ nodes }/>
{/if}

<g 
  class='bee-group'
  transform={`translate(-35, 0)`}
>
  <g class='nodes'>
    {#each nodes as node}
      {@const highlightAnimation = renderCta && userTakingTooLong && node.abbr === 'WA'}
      {@const fadeOpacity = renderCta && userTakingTooLong && node.abbr !== 'WA'}
      <g 
        class={`
          node-group 
          node-group-${node.abbr} 
          ${(activeState === node.abbr) || highlightAnimation  ? 'active' : ''} 
          ${hoverState || fadeOpacity ? 'hover' : ''}`
        } 
        transform={`translate(${node.x}, ${node.y})`}
        on:click={(e) => handleClick(e, node)}
        on:mouseenter={(e) => handleMouseEnter(e, node)}
        on:mouseleave={handleMouseOut}
      >
        <!-- svelte-ignore component-name-lowercase -->
        <path
          class='node'
          fill={ node.fillR }
          d={ node.rightPathString }
        ></path>
        <!-- svelte-ignore component-name-lowercase -->
        <path
          class='node'
          fill={ node.fillL }
          d={ node.leftPathString }
        ></path>
        <!-- svelte-ignore component-name-lowercase -->
        <path
          class='node node-stroke'
          fill={ 'none' }
          stroke={ 'black' }
          d={ node.fullPath }
        ></path>
        <text 
          class={`state-label ${labelActive ? 'active' : ''}`}
          dx={ (node.r_L + 3) * Math.cos(3 * Math.PI / 4 ) }
          dy={ -(node.r_L + 3) * Math.cos(3 * Math.PI / 4 ) }
        >
          {node.abbr}
        </text>
        {#if renderCta && userTakingTooLong && node.abbr === 'WA'}
          <g class='cta-container'>
            <ClickCta message="Click for more" />
          </g>
        {/if}
      </g>
    {/each}
  </g>
  <g class='values'>
    {#each nodes as node}
      <g transform={`translate(${node.x}, ${node.y})`}>
        {#if activeState === node.abbr}
          <text
            class="state-hover-value state-hover-value-L"
            x={ (node.r_L + 3) * Math.cos(3 * Math.PI / 4 ) + 8 }
            y={ (node.r_L + 3) * Math.cos(3 * Math.PI / 4 ) }
          >
            {percent(node.data.left_pct)}
          </text>
          <text
            class="state-hover-value state-hover-value-L"
            x={ (node.r_L + 3) * Math.cos(3 * Math.PI / 4 ) + 8 }
            y={ (node.r_L + 3) * Math.cos(3 * Math.PI / 4 ) }
            dy={ -13 }
          >
            {formatThousands2SI(node.data.left_size)}
          </text>
          <text
            class="state-hover-value state-hover-value-R"
            x={ -(node.r_R + 3) * Math.cos(3 * Math.PI / 4 ) - 8 }
            y={ (node.r_R + 3) * Math.cos(3 * Math.PI / 4 ) }
          >
            {percent(node.data.right_pct)}
          </text>
          <text
            class="state-hover-value state-hover-value-R"
            x={ -(node.r_R + 3) * Math.cos(3 * Math.PI / 4 ) - 8 }
            y={ (node.r_R + 3) * Math.cos(3 * Math.PI / 4 ) }
            dy={ -13 }
          >
            {formatThousands2SI(node.data.right_size)}
          </text>
        {/if}
      </g>
    {/each}
  </g>
</g>

<style lang='scss'>
  .node-group {
    transition: 0.5s opacity;
  }

  .node-group.hover.active {
    opacity: 1;
  }

  .node-group.hover {
    opacity: 0.6;
  }

  .node {
    stroke: $true-black;
    stroke-width: 0;
    cursor: pointer;
  }

  .node-stroke {
    stroke-width: 0;
    transition: 0.5s stroke-width;
  }

  .state-label {
    text-anchor: end;
    @include fs-xxs;
    transform: translate(0, 4px);
    opacity: 0;
    transition: opacity 0.5s;
    fill: $true-black;
  }

  .state-hover-cta {
    @include fs-xxs;
  }

  .state-label.active {
    opacity: 1;
    pointer-events: none;
  }

  .node-group:hover {
    .node-stroke {
      stroke-width: 1.25px
    }

    .state-label {
      font-weight: 700;
    }
  }

  .cta-container {
    animation: move 1s ease-in-out infinite alternate;
  }

  .state-hover-value {
    @include fs-sm;
    font-weight: 700;
    stroke: $white;
    stroke-width: 2pt;
    paint-order: stroke;
  }

  .state-hover-value-L {
    text-anchor: end;
    fill: $css-lab-dark-blue
  }

  .state-hover-value-R {
    fill: $css-lab-dark-red
  }

  @keyframes move {
    from {
      transform: translate(0, 0);
    }
    to {
      transform: translate(20px, 20px);
    }
  }
</style>
