<script lang="ts">
	// @ts-ignore
    import Header from '$lib/components/header/Header.svelte'
	// @ts-ignore
	import Footer from '$lib/components/footer/Footer.svelte';
</script>

<Header />

<main>
	<slot></slot>
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
</style>
