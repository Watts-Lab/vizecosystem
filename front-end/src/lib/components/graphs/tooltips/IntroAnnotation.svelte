<script lang="ts">
  // node_modules
	import { getContext } from 'svelte';

  const { width, height } = getContext('LayerCake')

  export let data : any[]

  function hide() { render = false }

  $: render = true

  const newYork = data.filter(d => d.abbr === 'NY')
  const northDakota = data.filter(d => d.abbr === 'ND')
  const maryland = data.filter(d => d.abbr === 'MD')
  
</script>

{#if render}
  <g 
    class='intro-annotation' 
  >
    <foreignObject class='foreign-object' width={$width} height={$height}>
      <div class='annotation-wrapper'>
        {#each newYork as node, i}
          <div class='annotation' style="top: {node.y - (node.r_L + 95)}px; left: {node.x - (node.r_L + 80)}px; transform: translate(-35px, 0)">
            In <b>NY</b>, 5 to 10% of the population
            experience partisanship in their news
            diets.
          </div>
        {/each}
        {#each northDakota as node, i}
          <div class='annotation' style="top: {node.y - (node.r_L + 140)}px; left: {node.x + (node.r_R + 20)}px; transform: translate(-35px, 0)">
            <b>ND</b>'s right-leaning echo chamber is
            much more sizeable and intense: over 
            10% of the population.
            <div class='close-button' on:click={hide}></div>
          </div>
        {/each}
        {#each maryland as node, i}
          <div class='annotation' style="top: {node.y - (node.r_L - 235)}px; left: {node.x + (node.r_R)}px; transform: translate(-35px, 0)">
            <b>MD</b> is the most left-leaning state after DC.
          </div>
        {/each}
      </div>
    </foreignObject>
    {#each newYork as node, i}
      <line 
        class='annotation-line' 
        x1={node.x - (node.r_L + 5)} 
        x2={node.x - (node.r_L - 10)} 
        y1={node.y - (node.r_L + 16)} 
        y2={node.y - (node.r_L - 16)} 
        transform={`translate(-35, 0)`}
      ></line>
    {/each}
    {#each northDakota as node, i}
      <line 
        class='annotation-line' 
        x1={node.x + (node.r_R + 45)} 
        x2={node.x - (node.r_L - 35)} 
        y1={node.y - (node.r_L + 45)} 
        y2={node.y - (node.r_L)} 
        transform={`translate(-35, 0)`}
      ></line>
    {/each}
    {#each maryland as node, i}
      <line 
        class='annotation-line'
        x1={node.x + (node.r_R + 50)} 
        x2={node.x - (node.r_L - 50)} 
        y1={node.y - (node.r_L - 225)} 
        y2={node.y - (node.r_L - 65)} 
        transform={`translate(-35, 0)`}
      ></line>
    {/each}
  </g>
{/if}

<style lang="scss">
  .foreign-object {
    transform: translateZ(0);
  }

  .annotation {
    background: white;
    padding: 2px 5px;
    box-shadow: 0 0 5px rgba(black, 0.2);
    pointer-events: all;
  }

  .annotation-line {
    stroke: black;
    stroke-width: 1pt;
  }

  .annotation-wrapper {
    width: 100%;
    height: 100%;
    position: relative;
    pointer-events: none;

    .annotation {
      @include fs-sm;
      position: absolute;
      max-width: 135px;
    }
  }

  .close-button {
    position: absolute;
    top: 0;
    right: 2px;
    pointer-events: all;
  }

  .close-button:after {
    content: '\2715';
    @include fs-root;
    line-height: 1;
  }
</style>