<script lang="ts">
	// import local data
	import data from '$lib/data/copy.json'
	import authors from '$lib/data/authors.json'

    // components
	import Title from '$lib/components/copy/Title.svelte';
	import Description from '$lib/components/copy/Description.svelte';
	import Authors from '$lib/components/copy/Authors.svelte';
	import Menu from '$lib/components/section-menu/Menu.svelte';

	import hash from '$lib/utils/hasher';

	$: auth = false;
	$: val = null;

	function authenticate(e) {
		e.preventDefault();
		if (hash(val) === '7cc1c93bdeaf85793bfe1bfbd33356e252c28bfe') {
			auth = true;
		}
	}
</script>


{#if auth}
	<div class='header-wrapper main-column'>
		<Title title={ data.title }></Title>
		<Description 
			content={ 
				data.intro
					.filter(d => d.type !== 'tiles') 
			}
		></Description>
		<Authors authors={ authors }></Authors>
	</div>

	<Menu tiles={data.intro.filter(d => d.type === 'tiles')} />

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

<style lang='scss'>
    .header-wrapper {
		@include grid-mobile;
		@include centerH;
		align-items: center;

		@media (min-width: $bp-3) {
			@include grid-main;
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