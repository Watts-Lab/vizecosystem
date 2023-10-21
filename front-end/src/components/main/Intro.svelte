<script lang="ts">
    // components
	import Title from '../copy/Title.svelte';
	import Description from '../copy/Description.svelte';
	import Authors from '../copy/Authors.svelte';
	import Menu from '../section-menu/menu.svelte';

    // types
	import type Author from '../../types/Authors';

    // prop declaration
	export let title : string;
	export let standfirst : any[] = [{value: 'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Commodi consequatur inventore exercitationem ex perferendis provident, earum cumque maiores quam quidem labore, mollitia odit eaque laborum?'}]
	export let authors : Author[];
	export let modal: any
</script>


<section>
    <div class='header-wrapper main-column'>
        <Title title={ title }></Title>
        <Description standfirst={ standfirst }></Description>
        <Authors authors={ authors }></Authors>
    </div>

	<Menu bind:modal />
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
			margin-top: 120px;
		}
	}

	.title-container {
		@include centerH;
		display: flex;
		gap: 25px;
	}

</style>