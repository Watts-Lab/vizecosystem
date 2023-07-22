<script>
  import { getContext } from 'svelte';
  import { area } from 'd3-shape';

  const { data, xGet, yScale, zGet } = getContext('LayerCake');
  
  $: areaGen = area()
    .x(d => $xGet(d))
    .y0(d => $yScale(d[0]))
    .y1(d => $yScale(d[1]));

</script>

<g class='vis'>
  {#each $data as d, i}
    <g class="area-group">
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