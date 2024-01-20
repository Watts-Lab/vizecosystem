<script lang="ts">
	// import local data
	import data from '../../data/copy.json'
	import authors from '../../data/authors.json'

    // components
	import Title from '../copy/Title.svelte';
	import Description from '../copy/Description.svelte';
	import Authors from '../copy/Authors.svelte';
	import Menu from '../section-menu/Menu.svelte';

	import hash from '../../utils/hasher';

	// prop declaration
	export let modal: any

	$: auth = true;
	$: val = null;

	function authenticate(e) {
		e.preventDefault();
		if (hash(val) === '7cc1c93bdeaf85793bfe1bfbd33356e252c28bfe') {
			auth = true;
		}
	}
</script>


<section>
	{#if auth}
		<div class='header-wrapper main-column'>
			<Title title={ data.title }></Title>
			<Description 
				content={ 
					data.intro
						.filter(d => d.type !== 'tiles') 
				}
				bind:modal
			></Description>
			<Authors authors={ authors }></Authors>
		</div>

		<Menu tiles={data.intro.filter(d => d.type === 'tiles')} bind:modal />

		{:else} <div class='auth'>
			<form on:submit={authenticate} >
				<input 
					type='password' 
					placeholder='password'	
					on:input={e => val = e.target.value} 
				/>
			</form>
		</div>
	{/if}
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

	.auth {
		height: 800px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>