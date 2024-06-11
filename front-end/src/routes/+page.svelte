<script lang="ts">
	// import local data
	import data from '$lib/data/copy.json'
	import authors from '$lib/data/authors.json'

    // components
	import Title from '$lib/components/copy/Title.svelte';
	import Description from '$lib/components/copy/Description.svelte';
	import Authors from '$lib/components/copy/Authors.svelte';
	import Menu from '$lib/components/section-menu/Menu.svelte';
</script>


<div class='header-wrapper main-column'>
	<Title title={ data.title }></Title>
	<Description 
		content={ 
			data.intro
				.filter(d => d.type !== 'tiles') 
		}
	></Description>
</div>

<Menu tiles={data.intro.filter(d => d.type === 'tiles')} />

<div class='header-wrapper main-column authors-wrapper'>
	<Authors authors={ authors }></Authors>
</div>

<style lang='scss'>
    .header-wrapper {
		@include grid-mobile;
		@include centerH;
		align-items: center;

		@media (min-width: $bp-3) {
			@include grid-main;
		}
	}
	.authors-wrapper {
		row-gap: 0;
	}

	.title-container {
		@include centerH;
		display: flex;
		gap: 25px;
	}
</style>