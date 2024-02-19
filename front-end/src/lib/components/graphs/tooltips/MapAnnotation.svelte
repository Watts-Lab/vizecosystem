<script lang="ts">
  // node_modules
	import { getContext } from 'svelte';
  import { path } from 'd3-path';

  // utils
  import getBrowserInfo from "$lib/utils/system-info";

  // dimensions
  const { width, height } = getContext('LayerCake')

  export let data : any[]

  function hide() { render = false }

  $: render = true
  $: browserInfo = getBrowserInfo()
  $: dy = (browserInfo === 'Chrome') || (browserInfo === 'Firefox') ? 0 : -50

  const newYork = data.filter(d => d.abbr === 'NY')
  const northDakota = data.filter(d => d.abbr === 'ND')
  const maryland = data.filter(d => d.abbr === 'MD')

  function curveGen(context, start, ref, end) {
    context.moveTo(start.x, start.y)
    context.bezierCurveTo(ref.x, ref.y, ref.x, ref.y, end.x, end.y)
    return context
  }
</script>

{#if render}
  <g 
    class='intro-annotation' 
  >
    <foreignObject class='foreign-object' width={$width} height={$height}>
      <div class='annotation-wrapper'>
        {#each newYork as node, i}
          <div class='annotation' style="top: {node.y - (node.r_L + 95)}px; left: {node.x - (node.r_L + 80)}px; transform: translate(-35px, {dy}px)">
            In <b>NY</b>, 5 to 10% of the population
            experience partisanship in their news
            diets.
          </div>
        {/each}
        {#each northDakota as node, i}
          <div class='annotation' style="top: {node.y - (node.r_L + 140)}px; left: {node.x + (node.r_R + 20)}px; transform: translate(-35px, {dy}px)">
            <b>ND</b>'s right-leaning echo chamber is
            much more sizeable and intense: over 
            10% of the population.
            <div class='close-button' on:click={hide}></div>
          </div>
        {/each}
        {#each maryland as node, i}
          <div class='annotation' style="top: {node.y - (node.r_L - 235)}px; left: {node.x + (node.r_R)}px; transform: translate(-35px, {dy}px)">
            <b>MD</b> is the most left-leaning state after DC.
          </div>
        {/each}
        <div class='annotation' style="top: 460px; left: 45px; transform: translate(-35px, {dy}px)">
          <b>Fox News</b> dominates in almost every state.
        </div>
      </div>
    </foreignObject>
    {#each newYork as node, i}
      <path
        class='annotation-line' 
        d={curveGen(
          path(), 
          {x: node.x - (node.r_L + 5), y: node.y - (node.r_L + 16)}, 
          {x: node.x - (node.r_L + 5), y: node.y - (node.r_L + 6)}, 
          {x: node.x - (node.r_L - 10), y: node.y - (node.r_L - 16)}
        )}
        transform={`translate(-35, 0)`}
      />
    {/each}
    {#each northDakota as node, i}
      <path
        class='annotation-line' 
        d={curveGen(
          path(), 
          {x: node.x + (node.r_R + 40), y: node.y - (node.r_L + 45)}, 
          {x: node.x + (node.r_R + 40), y: node.y - (node.r_L + 35)},
          {x: node.x - (node.r_L - 30), y: node.y - (node.r_L)}
        )}
        transform={`translate(-35, 0)`}
      />
    {/each}
    {#each maryland as node, i}
      <path
        class='annotation-line' 
        d={curveGen(
          path(), 
          {x: node.x + (node.r_R - 5), y: node.y - (node.r_L - 265)}, 
          {x: node.x - (node.r_R - 35), y: node.y - (node.r_L - 265)}, 
          {x: node.x - (node.r_L - 25), y: node.y - (node.r_L - 70)}
        )}
        transform={`translate(-35, 0)`}
      />
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
    fill: none;
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