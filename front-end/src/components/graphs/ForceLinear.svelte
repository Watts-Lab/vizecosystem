<script>
    import { getContext, createEventDispatcher } from 'svelte';
    import { geoAlbersUsa } from 'd3-geo'
    import { forceSimulation, forceCollide, forceManyBody } from 'd3-force';
    import { scaleOrdinal } from 'd3-scale';

  
    const { height, width, rScale, zScale, data, } = getContext('LayerCake');

    export let collideStrength = 1;
    export let manyBodyStrength = 1;
    // export let political_lean;
    export let medium;
    export let diet_threshold;
    export let partisanship_scenario;
    export let political_lean;

    // instantiate event dispatcher
    const dispatch = createEventDispatcher();

    // instantiate projection
    const projection = geoAlbersUsa()
      projection.translate([ $width / 2, $height / 2 ]);

    function restart() {
      simulation.alpha(1).restart();
    }

    // console.log($data)

    // variable declaration
    let rRatio = 2;
    let simulationStopped = false;
    let nodes = []
    let simulation = forceSimulation()
      .alpha(0)
      .alphaMin(0.4)
      .force(
        'collide', 
        forceCollide(d => d.r + rRatio * 5)
          .strength(collideStrength)
          .iterations(2)
      )
      .force('charge', forceManyBody().strength(manyBodyStrength));

    $: nodes = $data.map((d, i) => {
      const [ x, y ] = projection(d.coordinates)
      return ({ ...d, 
        x, 
        y,
        r: $rScale(d.data[`${lean}_pct`])
      })
    });
    
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
      nodes = $data.map((d, i) => {
        const [ x, y ] = projection(d.coordinates)
        return ({ ...d, 
          x, 
          y,
          r: $rScale(d.data[`${lean}_pct`])
        })
      });
      restart()
    }

    $: labelActive = false;

    $: lean = political_lean === 'R' ? 'right' : 'left';

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

</script>

<g 
  class='bee-group'
>

  {#each nodes as node}
    {@const fill = $zScale(node.data.right_pct)}
    <g class='node-group' transform={`translate(${node.x}, ${node.y})`}>
      <circle
        class='node'
        fill={ fill }
        cx={ 0 }
        cy={ 0 }
        r={ node.r }
        on:click={(e) => handleClick(e, node)}
      >
      </circle>
      <text 
        class={`state-label ${labelActive ? 'active' : ''}`}
        fill={scaleTypeColor(fill)}
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
    transition: 0.5s stroke-width;
    cursor: pointer;
  }

  .state-label {
    text-anchor: middle;
    @include fs-xs;
    transform: translate(0, 4px);
    opacity: 0;
    transition: opacity 1s;
  }

  .state-label.active {
    opacity: 1;
    pointer-events: none;
  }

  .node-group:hover {
    .node {
      stroke-width: 4px
    }

    .state-label {
      font-weight: 700;
    }
  }
</style>
<!-- on:mouseenter={(e) => handleMouseEnter(e, node)}
on:focus={(e) => handleMouseLeave(e, node)}
on:mouseleave={(e) => handleMouseLeave(e)}
on:blur={(e) => handleMouseLeave(e)} -->