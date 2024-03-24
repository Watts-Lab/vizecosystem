<script lang='ts'>
  import { getContext } from 'svelte';
  import { line, area, curveBasis } from 'd3-shape';

  import { mediumMap, politicsMap } from '$lib/utils/labels';

  const { data, xGet, yGet, yScale, zScale } = getContext('LayerCake');

  // prop declaration
  export let activeChart : string;
  export let minDate : Date;
  export let maxDate : Date;
  let highlightBand: boolean|string = false
  
  // variable declaration

  $: path = line()
    .x((d: any) => $xGet(d))
    .y((d: any) => $yGet(d))
    .curve(curveBasis)

  $: polygon = area()
    .x((d: any) => $xGet(d))
    .y0((d: any) => $yGet(d))
    .y1((d: any) => $yScale(d.value_2))
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
  
  function fade(node, { from, to }, { delay, duration }) {
    return {
      delay,
      duration,
      css: (t, u) =>
        `opacity: ${1 * t}`
    };
  }

  function parsePolygonData(d) {
    const [_50, _75] = d

    return _75[1].map((d, i) => {
      return { ...d, value_2: _50[1][i]['value'] }
    })
  }

  $: highlight = false
  $: highlightBand = false
</script>

<g class='line-group line-group-{activeChart}'>
  {#each $data as leanGroup, i}
    <g class='line-group-lean line-group-lean-{leanGroup[0]}'>
      {#each leanGroup[1] as mediumGroup, j}
        {@const fill = mediumGroup[0] === 'tv' ? `url(#diagonalHatch${leanGroup[0]})` : $zScale(leanGroup[0]) }
        <g 
          class='line-group-medium line-group-medium-{mediumGroup[0]} {highlight && highlightBand !== `${leanGroup[0]}-${mediumGroup[0]}` ? 'fade' : ''}'
          role="figure" 
          on:mouseenter={() => { highlight = true; highlightBand = `${leanGroup[0]}-${mediumGroup[0]}` }}
          on:mouseleave={() => { highlight = false; }}
          on:focus={() => highlight = mediumGroup[0]}
        >
          <!-- These each blocks are "faked" to allow the animate directive -->
          {#each [0] as d, l (`line-${leanGroup[0]}-${mediumGroup[0]}`)} 
            <path
              class={`path-line path-line-${mediumGroup[0]}`}
              d={ path(mediumGroup[1].get(50).filter(e => +e.date >= minDate && +e.date <= maxDate)) }
              stroke={ $zScale(leanGroup[0]) }
              animate:drawPath={{ delay: 0, duration: 500 }}
            ></path>
          {/each}
          {#each [0] as d, l (`polygon-${leanGroup[0]}-${mediumGroup[0]}`)} 
            <path
              class={`path-polygon path-polygon-${mediumGroup[0]}`}
              d={ polygon(
                parsePolygonData(mediumGroup[1]).filter(e => +e.date >= minDate && +e.date <= maxDate)
              )}
              { fill }
              animate:fade={{ delay: 500, duration: 500 }}
            ></path>
          {/each}
          {#if highlight && highlightBand === `${leanGroup[0]}-${mediumGroup[0]}`}
            {@const tgtPoint = mediumGroup[1].get(50).slice(-10)[0]}
            <text
              class='line-label'
              x={$xGet(tgtPoint)} 
              y={$yGet(tgtPoint)} 
              dy={-10}
            >
              {politicsMap.get(leanGroup[0])}, {mediumMap.get(mediumGroup[0])}
            </text>
          {/if}
        </g>
      {/each}
    </g>
  {/each}
</g>
  

<style lang='scss'>
  .line-group-medium.fade {
    opacity: 0.35;
  }

  .path-line {
      fill: none;
      stroke-linejoin: round;
      stroke-linecap: round;
      stroke-width: 1.5;
  }

  .path-polygon {
    fill-opacity: 0.35
  }

  .line-label{
    @include fs-base;
    text-anchor: middle;
    paint-order: stroke;
    stroke: $off-white;
    stroke-width: 2pt;
  }
</style>
