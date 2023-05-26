<script>
    import { getContext, createEventDispatcher } from 'svelte';
    import { geoAlbersUsa } from 'd3-geo'
    import { forceSimulation, forceCollide, forceManyBody } from 'd3-force';
    import { scaleOrdinal } from 'd3-scale';
    import { path } from 'd3-path'
  
    const { height, width, rScale, zScale, data } = getContext('LayerCake');

    export let collideStrength = 1;
    export let manyBodyStrength = 1;
    // export let political_lean;
    export let medium;
    export let diet_threshold;
    export let partisanship_scenario;

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
        const r = $rScale(Math.abs(d.data.value))
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

    function handleMouseEnter(e, d) {
      dispatch('mouseenter', { target: e.target, node: d })
    }

    function handleClick(e, d) {
      dispatch('click', { target: e.target, node: d })
    }

    function handleMouseLeave(e) {
      dispatch('mouseleave')
    }

    const scaleTypeColor = scaleOrdinal()
      .domain($zScale.range())
      .range(['gainsboro', 'gainsboro', 'black', 'gainsboro', 'gainsboro'])

    function arcGen(context, pos) {
      context.arc(0, 0, pos.r, pos.start, pos.end)
      context.closePath()
      return context;
    }

    function pathGen(context, pos1, pos2) {
      context.arc(0, 0, pos1.r, -Math.PI/2, Math.PI/2)
      context.arc(0, 0, pos2.r, Math.PI/2, -Math.PI/2)
      context.closePath()
      return context
    }

</script>

<g 
  class='bee-group'
>
  {#each nodes as node}
    <g 
      class='node-group' 
      transform={`translate(${node.x}, ${node.y})`}
      on:click={(e) => handleClick(e, node)}
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
        fill='black'
        dx={ (node.r_L + 3) * Math.cos(3 * Math.PI / 4 ) }
        dy={ -(node.r_L + 3) * Math.cos(3 * Math.PI / 4 ) }
      >
        {node.abbr}
      </text>
    </g>
  {/each}
</g>

<style lang='scss'>
  .node {
    stroke: $true-black;
    stroke-width: 0;
    // transition: 0.5s stroke-width;
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
  }

  .state-label.active {
    opacity: 1;
    pointer-events: none;
  }

  .node-group:hover {
    .node-stroke {
      stroke-width: 1px
    }

    .state-label {
      font-weight: 700;
    }
  }
</style>
