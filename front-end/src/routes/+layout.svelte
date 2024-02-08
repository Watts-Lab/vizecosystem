<script lang="ts">
	// @ts-ignore
    import Header from '$lib/components/header/Header.svelte'
	// @ts-ignore
	import Footer from '$lib/components/footer/Footer.svelte';

	import hash from '$lib/utils/hasher';

	$: auth = true;
	$: val = null;

	function authenticate(e) {
		e.preventDefault();
		if (hash(val) === '7cc1c93bdeaf85793bfe1bfbd33356e252c28bfe') {
			auth = true;
		}
	}
</script>

<Header />

<main>
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
		margin: 25px auto;
		
		@media (min-width: $bp-3) {
			margin-top: 60px;
		}
	}

	.auth {
		height: 800px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
