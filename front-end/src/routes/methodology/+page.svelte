<script lang="ts">
	// import local data
	import copy from '$lib/data/copy.json';
	const data: any = copy['methodology'];
	
	// utils
	import parseCopy from '$lib/utils/parse-copy';
</script>

<section class="section">
	{#each data as d}
		{#if d.type === 'text'}
			<p class="copy">
				{@html parseCopy(d.value)}
			</p>
		{:else if d.type === 'title'}
			<h1 class="section-title">{d.value}</h1>
		{:else if d.type === 'references'}
			<div class="references">
				<h3>References</h3>
				<div class="citation">
					{#each d.value as ref}
						<p class="citation-entry">
							{@html parseCopy(ref)}
						</p>
					{/each}
				</div>
			</div>
		{/if}
	{/each}
</section>

<style lang="scss">
	.section {
		grid-template-columns: repeat(12, 1fr);
		column-gap: 15px;
	}

	.section-title {
		@include fs-xl;
		grid-row: 1 / span 1;
		grid-column: 3 / span 8;
		margin-bottom: 1em;
	}

	.copy {
		grid-column: span 12;

		@media (min-width: $bp-3) {
			grid-column: 3 / span 8;
		}
	}

	.references {
		grid-column: span 12;

		@media (min-width: $bp-3) {
			grid-column: 3 / span 8;
		}

		.citation {
			padding: 0 0 0 1.5em;
			border-left: 3pt solid $mid-grey;

			.citation-entry {
				@include fs-root;
			}
		}
	}

	p {
		margin-top: 0;
		margin-bottom: 1em;
		@include fs-root;

		@media (min-width: $bp-3) {
			@include fs-md;
		}
	}
</style>
