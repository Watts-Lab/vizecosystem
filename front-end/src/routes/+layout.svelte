<script lang="ts">
	// @ts-ignore
    import Header from '$lib/components/header/Header.svelte'
	// @ts-ignore
	import Footer from '$lib/components/footer/Footer.svelte';
	
	import { dev } from '$app/environment';
	import { page } from '$app/stores';

	import hash from '$lib/utils/hasher';

	$: auth = dev || false;
	$: val = null;

	function authenticate(e: Event) {
		e.preventDefault();
		if (hash(val) === '7cc1c93bdeaf85793bfe1bfbd33356e252c28bfe') {
			auth = true;
		}
	}
</script>

<Header />

<main class:index={$page.route.id === '/'} class:section={$page.route.id !== '/'}>
	{#if auth} <slot></slot>

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
</main>

<Footer />


<style lang='scss'>
    main {
		max-width: $column-width;
		margin: 25px auto 0 auto;
	}

	.index {
		@media (min-width: $bp-4) {
			margin: 60px auto 0 auto;
			max-width: $column-width * 1.2;
		}
	}

	.section {
		@media (min-width: $bp-4) {
			margin: 60px auto 0 auto;
			max-width: $column-width;
		}
	}

	.auth {
		height: 800px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
