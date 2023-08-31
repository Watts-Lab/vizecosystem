<script lang='ts'>
  import { getContext } from 'svelte';
  import { line, curveBasis } from 'd3-shape';

  const { data, xGet, yGet, xScale, yScale, zScale } = getContext('LayerCake');

  // prop declaration
  export let activeChart : string;

  $: path = line()
    .x(d => $xGet(d))
    .y(d => $yGet(d))
    .curve(curveBasis)

  function drawPath(node, { from, to }, { delay, duration }) {
    const len = node.getTotalLength();
    return {
      delay,
      duration,
      css: (t, u) =>
        `stroke-dasharray: ${t * len} ${u * len}`
    };
  }

</script>

<g class={`line-group line-group-${activeChart}`}>
  {#each $data as group, i}    
      {@const areaData = group[1][0][1]
        .map((d, i) => ({ ...d, value_2: group[1][1][1][i]['value'] }))
      }
      <g class='threshold-group threshold-group-{group[0]}'>
        {#each group[1] as d, l (d)}
          <path
            class={`path-line path-line-${d[0]}`}
            d={ path(d[1]) }
            animate:drawPath={{ delay: 0, duration: 500 }}
          ></path>
        {/each}
    </g>
  {/each}
</g>
  

<style lang='scss'>
  .path-line {
    fill: none;
    stroke-linejoin: round;
    stroke-linecap: round;
    stroke-width: 1.5px;
  }

  .path-line-L {
    stroke: blue;
  }
  .path-line-R {
    stroke: red;
  }


  .threshold-group-online {
    .path-line {
      stroke-dasharray: 4 1
    }
  }
</style>
