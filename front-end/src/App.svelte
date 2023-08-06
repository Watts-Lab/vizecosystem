<script lang="ts">
	// types
	import type Data from './types/Data';
	import type Author from './types/Authors';

	// sections
	import Header from './components/header/Header.svelte';
	import Footer from './components/footer/Footer.svelte';
	import Main from './components/main/Main.svelte';
	import Section1 from './components/main/Section1.svelte';
	import Section2 from './components/main/Section2.svelte';
	import Section3 from './components/main/Section3.svelte';

	// export let title : string = 'Your title goes here';
	// export let standfirst : any[]
	export let data : Data
	export let authors : Author[];
</script>

<Header />
<Main 
	title={ data.title } 
	{ authors } 
	standfirst={ data.standfirst }
	captions={ data['main-section'].captions }
/>
<Section1 
	once={ true } 
	copy={data['section-one'].copy} 
	refs={data['section-one'].references} 
	captions={data['section-one'].captions} 
/>
<Section2 once={ true } copy={data['section-two'].copy} refs={data['section-two'].references} captions={data['section-two'].captions} />
<Section3 once={ true } copy={data['section-three'].copy} refs={data['section-three'].references} captions={data['section-three'].captions} />
<Footer />

<style lang='scss' global>
	main, .section {
		padding: 0 1em;
	}
	@media (min-width: $column-width) {
		main, .section {
			padding: 0
		}
	}
	.section {
		max-width: $column-width;
		margin: 3em auto;
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

	.chart-mini, .popup-overlay {
		height: 100%;
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