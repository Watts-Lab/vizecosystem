<script lang="ts">
    // import local data
	import copy from '$lib/data/copy.json'
    const data: any = copy['methodology'];

	import parseCopy from '$lib/utils/parse-copy';
</script>

<section class='section'>
	{#each data as d, i}
		{#if d.type === 'text'}
			<p class='copy'>
				{@html parseCopy(d.value)}
			</p>
        {:else if d.type === 'title'} <h1 class='section-title'>{ d.value }</h1>
		{/if}
	{/each}
</section>

<style lang='scss'>
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

	p {
		margin-top: 0;
		margin-bottom: 1em;
		@include fs-root;

		@media (min-width: $bp-3) {
			@include fs-md;
		}
	}

	.title-container {
		grid-column: span 12;

		h3 {
			margin-bottom: 1em;
		}
	}
</style>
