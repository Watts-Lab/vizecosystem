<script lang="ts">
    // node_modules
    import { zip }	from 'd3-array';

    // utils
    import { flowMap } from '$lib/utils/labels';

    export let seriesNames: string[];
    export let seriesColors: string[];

    $: legend = zip(seriesNames, seriesColors)
</script>


<div class='legend'>
    {#each legend as [name, color], i}
        <div class='legend-item'>
            <div class='legend-icon legend-icon-color legend-icon-color-{name}' style='--color: {color}'></div>
            <div>{flowMap.get(name)}</div>
        </div>
    {/each}
</div>

<style lang="scss">
    .legend {
		display: flex; 
		gap: 15px;
		margin-top: 15px;
		font-size: 14px;

		.legend-item {
			display: flex;
			align-items: center;
			gap: 5px;
			
			.legend-icon {
				width: 17.5px;
				height: 17.5px;
				border-radius: 3px;	
			}
        }

        .legend-icon-color {
            background-color: var(--color);
            opacity: 0.65;
        }
    }
</style>