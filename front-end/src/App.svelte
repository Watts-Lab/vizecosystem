<script lang="ts">
	import { fade } from 'svelte/transition';

	// sections
	import Header from './components/header/Header.svelte';
	import Footer from './components/footer/Footer.svelte';
	import Intro from './components/main/Intro.svelte';
	import Modal from './components/main/Modal.svelte'
	// import Main from './components/main/Main.svelte';
	// import Section2 from './components/main/Section1.svelte';
	// import Section1 from './components/main/Section2.svelte';
	// import Section3 from './components/main/Section3.svelte';
  	// import Supplementary from './components/main/Supplementary.svelte';

	// exporting properties
	export let modal: any;

	$: modal = false
	$: renderModal = modal && Object.hasOwn(modal, 'renderer')
	$: document.body.classList[renderModal ? 'add' : 'remove']('noscroll');
</script>

<div 
	class="body" 
	class:modalType={renderModal} 
	class:landingType={!renderModal}
>
	<Header />
	<main>
		<Intro bind:modal />
	</main>
	{#if renderModal}
		<Modal comp={ modal } bind:modal />
		<div 
			class='modal-background'
			in:fade
			out:fade
			on:click={() => {
				if (modal) modal = false;
			}}
		></div>
	{/if}

	<Footer />
</div>

<style lang='scss' global>
	main, .section {
		padding: 0 1em;
	}

	.body {
		position: relative;
	}

	.body.landingType {
		overflow-y: visible;
	}	

	.body.modalType {
		overflow-y: hidden;
	}

	@media (min-width: $column-width) {
		main, .section {
			padding: 0
		}
	}

	.modal-background {
		background-color: transparentize($black, 0.1);
		position: absolute;
		top: 0;
		height: 100%;
		left: 0;
		right: 0;
		z-index: 9998;
	}

	.section {
		max-width: $column-width;
		margin: 1em auto 3em auto;
		padding: 0.5em 2em;
		display: grid;
	}

	.main-column {
		max-width: $column-width;
		margin-left: auto;
		margin-right: auto;
	}

	.chart {
		height: 500px;
	}

	.chart-medium {
		height: 400px;
	}

	.chart-mini {
		height: 100%;
	}

	.popup-overlay {
		display: flex;
	}

	.chart-flow {
		height: 600px;
	}

	.small-multiples,
	.chart-large {
		height: 800px;
	}

	.caption {
		@include fs-sm;
		font-weight: 300;
	}

	.copy {
		margin: 0;

		@media (min-width: $bp-3) {
			margin: 35px 0;
		}

		p {
			margin: 10px 0;
			@include fs-root;

			@media (min-width: $bp-2) {
				@include fs-md;
			}
		}
	}

	.references {
		margin: 0;

		@media (min-width: $bp-3) {
			margin: 35px 0;
		}

		p {
			margin: 10px 0;
			line-height: 1.6;
			@include fs-sm;
		}
	}

	.link.inactive {
			stroke-opacity: 0.15 !important;
	}
	.link.active {
			stroke-opacity: 0.5 !important;
	}

	.heat-map-cell.active {
		border: 1pt solid $black !important;
	}

	.group-rect.inactive, 
	.range-circle.inactive {
        opacity: 0.5 !important;
    }
	
	.group-rect.active,
	.range-circle.active {
        opacity: 1 !important;
    }

	.active-node {
		stroke: black;
		stroke-width: 2pt; 
	}
</style>
