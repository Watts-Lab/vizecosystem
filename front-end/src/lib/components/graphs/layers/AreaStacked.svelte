<script>
  import { getContext } from 'svelte';
  import { area, curveBasis } from 'd3-shape';

  const { data, xGet, yScale, zGet } = getContext('LayerCake');
  
  $: areaGen = area()
    .x(d => $xGet(d))
    .y0(d => $yScale(d[0]))
    .y1(d => $yScale(d[1]))
    .defined(d => d[1] !== 0)
    .curve(curveBasis);

  function fade(node, { from, to }, { delay, duration }) {
    return {
      delay,
      duration,
      css: (t, u) =>
        `opacity: ${1 * t}`
    };
  }

</script>

<g class='vis'>
  {#each $data as d, i (d)}
    <g class="area-group" animate:fade={{ delay: 0, duration: 500 }}>
      <path
        class='path-area'
        d='{areaGen(d)}'
        fill='{$zGet(d)}'
        ></path>
    </g>
    
    
  {/each}
</g>

<style lang='scss'>
  .path-area {
    opacity: 0.95;
  }
</style>