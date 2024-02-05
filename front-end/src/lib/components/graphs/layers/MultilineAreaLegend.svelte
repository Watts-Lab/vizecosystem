<div class='legend'>
    {#each [50,75] as cat}
        <div class='legend-item'>
            <div class='legend-icon legend-icon-{cat}'></div>
            <div>{cat}% of diet</div>
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

            .legend-icon-50 {
                height: 1.5pt;
                background-color: $black;
            }

            .legend-icon-75 {
                background-color: transparentize($black, 0.5);
            }
		}
	}
</style>