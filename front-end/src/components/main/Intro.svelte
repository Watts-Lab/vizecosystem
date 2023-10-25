<script lang="ts">
	// import local data
	import data from '../../data/copy.json'
	import authors from '../../data/authors.json'

    // components
	import Title from '../copy/Title.svelte';
	import Description from '../copy/Description.svelte';
	import Authors from '../copy/Authors.svelte';
	import Menu from '../section-menu/Menu.svelte';

    // prop declaration
	export let modal: any
</script>


<section>
    <div class='header-wrapper main-column'>
        <Title title={ data.title }></Title>
        <Description content={ data.intro.filter(d => d.type !== 'tiles') }></Description>
        <Authors authors={ authors }></Authors>
    </div>

	<Menu tiles={data.intro.filter(d => d.type === 'tiles')} bind:modal />
</section>

<style lang='scss'>
    section {
		max-width: $column-width;
		margin: 0 auto;
	}

    .header-wrapper {
		@include grid-mobile;
		@include centerH;
		align-items: center;
		margin: 25px 0;

		@media (min-width: $bp-3) {
			@include grid-main;
			margin-top: 60px;
		}
	}

	.title-container {
		@include centerH;
		display: flex;
		gap: 25px;
	}

</style>