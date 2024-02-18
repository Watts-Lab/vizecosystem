<script lang="ts">
    // utils
    import labelMap from '$lib/utils/labels';

    // prop declaration
    export let dataMap: Map<any, any>
    export let colorMap: Map<any, any>
</script>

<div class='legend'>
    {#each Array.from(dataMap.keys()) as cat}
        <div class='legend-item'>
            <div class={'legend-color'} style='--color: {colorMap.get(cat)}'></div>
            <div>{labelMap.get(cat)}</div>
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
			
			.legend-color {
				background-color: var(--color);
				width: 13.5px;
				height: 13.5px;
				border-radius: 3px;
			}
		}
	}
</style>