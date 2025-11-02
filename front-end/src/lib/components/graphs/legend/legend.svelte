<script lang="ts">
    // utils
    import labelMap from '$lib/utils/labels';

    // prop declaration
    export let dataMap: Map<any, any>
    export let colorMap: Map<any, any>
    export let enabledSet: Set<string>
    export let toggleFilter: Function 
    
    // $: enabledMap = new Map(
    //   Array.from(dataMap.keys()).map(d => [d, true])
    // )
    // $: console.log(enabledMap)

    function click(cat: string) {
      // enabledMap = new Map(enabledMap)
      // enabledMap.set(cat, !enabledMap.get(cat))

      toggleFilter(cat)
    }

    function handleClick(event: any, data: { cat: string}) {
      // Check if the pressed key is the 'Enter' key or the 'Space' key
      if (event.key === 'Enter' || event.key === ' ') {
        click(data.cat)
      }
    }

</script>

<div class='legend'>
    {#each Array.from(dataMap.keys()).sort((a,b) => colorMap.get(a).order - colorMap.get(b).order) as cat}
        <div 
          class='legend-item'
          class:disabled={enabledSet.has(cat)}
          tabindex="0"
          role='button'
          on:click={() => click(cat)}
          on:keydown={(ev) => handleClick(ev, { cat })}
        >
            <div class='legend-color' style='--color: {colorMap.get(cat).color}'></div>
            <div class='legend-label'>{labelMap.get(cat)}</div>
        </div>
    {/each}
</div>

<style lang='scss'>
    .legend {
		flex-grow: 1;
		display: flex; 
		flex-wrap: wrap;
		column-gap: 15px;
		row-gap: 5px;
		align-items: flex-start;
    @include fs-sm;

		.legend-item {
			display: flex;
			align-items: center;
			gap: 5px;
      cursor: pointer;
			
			.legend-color {
				background-color: var(--color);
        border: 1pt solid var(--color);
				width: 13px;
				height: 13px;
				border-radius: 3px;
			}
		}

    .disabled {
      filter: grayscale(100%);

      .legend-label {
        text-decoration: line-through;
      }

			.legend-color {
        border: 1pt solid black;
				background-color: transparent 
      }
    }
	}
</style>
