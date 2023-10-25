<script lang="ts">
	// components
	import LinkButton from "./LinkButton.svelte";
	
	// property definitions
	export let content : any[];

</script>

<div class='intro-wrapper'>
	{#each content as text, i}
		{#if text.type === 'buttons'} 
			<div>Read the original research:

				{#each text.value as btn}
					<LinkButton { ...btn } />
				{/each}
			</div>
		{:else}
			<p>
				{ text.value } 
				{#if i === 0}
					<a href="#supplementary">Read more about the data.</a>
				{/if}
			</p>
		{/if}
	{/each}
</div>


<style lang='scss'>
	.intro-wrapper {
		grid-column: 1 / span 12;
		grid-row: 3 / span 1;
		
		@media (min-width: $bp-3) {
			grid-column: 1 / span 8;
		}

		p, div {
			margin-bottom: 1em;
			@include fs-root;

			@media (min-width: $bp-3) {
				@include fs-md;
			}
		}
		
		div {
			display: flex;
			gap: 5px;
			align-items: baseline;
			@include fs-base;
		}

	}
</style>