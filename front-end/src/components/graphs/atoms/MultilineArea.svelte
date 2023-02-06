<script lang='ts'>
  import { getContext } from 'svelte';
  import { line, area, curveBasis } from 'd3-shape';

  const { data, xGet, yGet, xScale, yScale, zScale } = getContext('LayerCake');

  // prop declaration
  export let activeChart : string;
  
  // variable declaration
  // $: animated = false

  $: path = line()
    .x(d => $xGet(d))
    .y(d => $yGet(d))
    .curve(curveBasis)

  $: polygon = area()
    .x(d => $xGet(d))
    .y0(d => $yGet(d))
    .y1(d => $yScale(d.value_2))


  function drawPath(node, { from, to }, { delay, duration }) {
    const len = node.getTotalLength();
    return {
      delay,
      duration,
      css: (t, u) =>
        `stroke-dasharray: ${t * len} ${u * len}`
    };
  }
  
  function fade(node, { from, to}, { delay, duration }) {
    return {
      delay,
      duration,
      css: (t, u) =>
        `opacity: ${1 * t}`
    };
  }
</script>

<g class={`line-group line-group-${activeChart}`}>
  {#each $data as group, i}    
      {@const areaData = group[1][0][1]
        .map((d, i) => ({ ...d, value_2: group[1][1][1][i]['value'] }))
      }
      {@const color = $zScale(group[0])}
      <g class='threshold-group threshold-group-{group[0]}'>
        {#each group[1].filter(e => e[0] === 50) as d, l (d)}
          <path
            class={`path-line path-line-${d[0]}`}
            d={ path(d[1]) }
            stroke={ color }
            animate:drawPath={{ delay: 0, duration: 500 }}
          ></path>
        {/each}
        {#each group[1].filter(e => e[0] === 50) as d, l (d)}
          <path
            class={`path-polygon path-polygon-${d[0]}`}
            d={ polygon(areaData) }
            fill={ color }
            animate:fade={{ delay: 500, duration: 500 }}
          ></path>
        {/each}
      </g>
  {/each}
</g>
  

<style>
  .path-line {
      fill: none;
      stroke-linejoin: round;
      stroke-linecap: round;
      stroke-width: 2;
  }

  .path-polygon {
    fill-opacity: 0.35
  }
</style>
