<script lang="ts">
  // node_modules
	import { onMount, getContext } from 'svelte';

  const { width, height } = getContext('LayerCake')

  export let data : any[]

  function hide() { render = false }

  onMount(() => {
    // setTimeout(hide, 5000)
  })

  $: render = true

  const newYork = data.filter(d => d.abbr === 'NY')
  const northDakota = data.filter(d => d.abbr === 'ND')
  
</script>

{#if render}
  <g class='intro-annotation'>
    <foreignObject width={$width} height={$height}>
      <div class='annotation-wrapper'>
        {#each newYork as node, i}
          <div class='annotation' style="top: {node.y - (node.r_L + 60)}px; left: {node.x - (node.r_L + 60)}px">
            In NY, 5 to 10% of the population
            experience partisan in their news
            diets.
          </div>
        {/each}
        {#each northDakota as node, i}
          <div class='annotation' style="top: {node.y - (node.r_L + 90)}px; left: {node.x + (node.r_R)}px">
            ND's right-leaning echo chamber is
            much more sizeable and intense: over 
            10% of the population.
          </div>
        {/each}
      </div>
    </foreignObject>
    <!-- <foreignObject></foreignObject> -->
  </g>
{/if}

<style lang="scss">
  .intro-annotation {
    pointer-events: none;
  }

  .annotation-wrapper {
    width: 100%;
    height: 100%;
    position: relative;

    .annotation {
      @include fs-xs;
      position: absolute;
      max-width: 100px;
    }
  }
</style>