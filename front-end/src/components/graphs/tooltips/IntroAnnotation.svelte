<script lang="ts">
  // node_modules
	import { getContext } from 'svelte';

  const { width, height } = getContext('LayerCake')

  export let data : any[]

  function hide() { render = false }

  $: render = true

  const newYork = data.filter(d => d.abbr === 'NY')
  const northDakota = data.filter(d => d.abbr === 'ND')
  
</script>

{#if render}
  <g 
    class='intro-annotation'
    transform={`translate(-35, 0)`}
  >
    <foreignObject width={$width} height={$height}>
      <div class='annotation-wrapper'>
        {#each newYork as node, i}
          <div class='annotation' style="top: {node.y - (node.r_L + 80)}px; left: {node.x - (node.r_L + 80)}px">
            In <strong>NY</strong>, 5 to 10% of the population
            experience partisanship in their news
            diets.
          </div>
        {/each}
        {#each northDakota as node, i}
          <div class='annotation' style="top: {node.y - (node.r_L + 140)}px; left: {node.x + (node.r_R + 20)}px">
            <strong>ND</strong>'s right-leaning echo chamber is
            much more sizeable and intense: over 
            10% of the population.
            <div class='close-button' on:click={hide}></div>
          </div>
        {/each}
      </div>
    </foreignObject>
    {#each newYork as node, i}
      <line class='annotation-line' x1={node.x - (node.r_L + 5)} x2={node.x - (node.r_L - 10)} y1={node.y - (node.r_L + 16)} y2={node.y - (node.r_L - 16)}></line>
    {/each}
    {#each northDakota as node, i}
      <line class='annotation-line' x1={node.x + (node.r_R + 45)} x2={node.x - (node.r_L - 35)} y1={node.y - (node.r_L + 45)} y2={node.y - (node.r_L)}></line>
    {/each}
  </g>
{/if}

<style lang="scss">
  .annotation-line {
    stroke: black;
    stroke-width: 1pt;
  }

  .annotation-wrapper {
    width: 100%;
    height: 100%;
    position: relative;

    .annotation {
      @include fs-sm;
      position: absolute;
      max-width: 125px;
    }
  }

  .close-button {
    position: absolute;
    top: -5px;
    right: 0;
  }

  .close-button:after {
    content: '\2715';
    @include fs-root;
    line-height: 1;
  }
</style>