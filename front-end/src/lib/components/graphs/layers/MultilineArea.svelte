<script lang='ts'>
  import { getContext } from 'svelte';
  import { line, area, curveBasis } from 'd3-shape';

  const { data, xGet, yGet, yScale, zScale } = getContext('LayerCake');

  // prop declaration
  export let activeChart : string;

  // $: console.log($data)
  
  // variable declaration

  $: path = line()
    .x(d => $xGet(d))
    .y(d => $yGet(d))
    .curve(curveBasis)

  $: polygon = area()
    .x(d => $xGet(d))
    .y0(d => $yGet(d))
    .y1(d => $yScale(d.value_2))
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
</script>

<g class='line-group line-group-{activeChart}'>
  {#each $data as leanGroup, i}
    <!-- {console.log(leanGroup)} -->
    <g class='line-group-lean line-group-lean-{leanGroup[0]}'>
      {#each leanGroup[1] as mediumGroup, j}
        {@const fill = mediumGroup[0] === 'tv' ? `url(#diagonalHatch${leanGroup[0]})` : $zScale(leanGroup[0]) }
        <g class='line-group-medium line-group-medium-{mediumGroup[0]}'>
          <path
            class={`path-line path-line-${mediumGroup[0]}`}
            d={ path(mediumGroup[1].get(50)) }
            stroke={ $zScale(leanGroup[0]) }
          ></path>
          <path
            class={`path-polygon path-polygon-${mediumGroup[0]}`}
            d={ polygon(
              parsePolygonData(mediumGroup[1])
            )}
            { fill }
            ></path>
            
        </g>
      {/each}
    </g>
  {/each}
</g>
  

<style>
  .path-line {
      fill: none;
      stroke-linejoin: round;
      stroke-linecap: round;
      stroke-width: 1.5;
  }

  .path-polygon {
    fill-opacity: 0.35
  }
</style>
