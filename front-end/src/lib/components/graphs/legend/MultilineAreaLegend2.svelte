<script lang="ts">
	// node_modules
	import { zip }	from 'd3-array';

	// utils
	import { politicsMap } from '$lib/utils/labels';

	export let seriesNames: string[];
	export let seriesColors: string[];

	$: legend = zip(seriesNames, seriesColors)
</script>

<div class='legend'>
    {#each legend as [name, color], i}
        <div class='legend-item'>
            <div class='legend-icon legend-icon-color legend-icon-color-{name}' style='--color: {color}'></div>
            <div>{politicsMap.get(name)}</div>
        </div>
    {/each}
	<div class='separator'></div>	
	{#each ['Desktop', 'TV'] as cat}
		<div class='legend-item'>
			<div class='legend-icon legend-icon-{cat}'></div>
			<div>{cat}</div>
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

            .legend-icon-Desktop {
                background-color: transparentize($black, 0.5);
            }
			
            .legend-icon-TV {
				background: repeating-linear-gradient(
					-45deg,
					$dark-grey 0%,
					$white 10%,
				);
            }

			.legend-icon-color {
				background-color: var(--color);
			}

		}

		.separator {
			border: 0.5px solid $mid-grey;
		}
	}
</style>