<script lang="ts">
	// @ts-ignore
    import Header from '$lib/components/header/Header.svelte'
	// @ts-ignore
	import Footer from '$lib/components/footer/Footer.svelte';
	
	import { page } from '$app/stores';
</script>

<Header />

<main class:index={$page.route.id === '/'} class:section={$page.route.id !== '/'}>
	<slot></slot>
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
