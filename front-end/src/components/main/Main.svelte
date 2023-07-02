<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { csv } from "d3-fetch";
  import { autoType } from "d3-dsv";
	import { group } from 'd3-array';
	import { scaleDiverging, scaleThreshold, scaleSqrt, scaleLinear } from 'd3-scale';

	// types
	import type Author from '../../types/Authors';
	import type ChartConfig from '../../types/ChartConfig';

	// components
	import Title from '../copy/Title.svelte';
	import Description from '../copy/Description.svelte';
	import Authors from '../copy/Authors.svelte';
	import ChartPlaceholder from '../global/chart-placeholder.svelte';
	
	// prop declaration
	export let title : string;
	export let standfirst : any[] = [{value: 'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Commodi consequatur inventore exercitationem ex perferendis provident, earum cumque maiores quam quidem labore, mollitia odit eaque laborum?'}]
	export let authors : Author[];

	// local data
	// import states from '../../data/states_centroids.json'
  

	// chart config
	
	let data : any[];
	let table : any[];
	let dataMap : Map<string, any>
	let fullDataMap : Map<string, any>
	const urlChart : string  = 'assets/data/EchoCh-by_state.csv'
	
	onMount(async () => {
		// load data for map + line chart
		const resChart = await csv(urlChart, autoType)
		data = resChart
    // parse data for 
		dataMap = group(
			data,
			d => d.period,
			d => d.state,
			d => d.medium, 
			d => d.diet_threshold,
			d => d.partisanship_scenario
		)

    fullDataMap = group(
			data,
			d => d.state,
			d => d.medium, 
			d => d.partisanship_scenario
		)
	})

	const chartConfig : Map<number,ChartConfig> = new Map([
		[0, {
			type: "diverging",
			rScale: scaleSqrt,
			rDomain: [1e3, 3e6],
			rRange: [10, 90],
			zScale: scaleThreshold,
			zDomain: [-0.1, -0.05, -0.01, 0.01, 0.05, 0.1],
			colorInterpolator: scaleDiverging,
			colorInterpolatorDomain: [-0.75, 0, 0.75],
			colorInterpolatorScheme: ["#011f5b", "gainsboro", "#990000"],
			colorPaletteAnchors: [-0.7, -0.35, -0.18, 0, 0.18, 0.35, 0.85]
		}],
		[1, {
			type: "linear",
			rScale: scaleSqrt,
			rDomain: [1e3, 3e6],
			rRange: [10, 90],
			zScale: scaleThreshold,
			zDomain: [0, 0.01, 0.025, 0.05],
			colorInterpolator: scaleLinear,
			colorInterpolatorDomain: [0, 1],
			colorInterpolatorScheme: "gainsboro",
			colorPaletteAnchors: [0, 0.25, 0.5, 0.75, 1]
		}],
	])

	$: chart = "0"
	$: activeChart = chartConfig.get(+chart)
	$: politicalChecked = true
</script>

<main>
	<div class='header-wrapper main-column'>
		<Title title={ title }></Title>
		<Description standfirst={ standfirst }></Description>
		<Authors authors={ authors }></Authors>
	</div>
	
	<ChartPlaceholder row={0}/>
</main>

<style lang='scss'>
	main {
		max-width: $column-width * 1.25;
		margin: 0 auto;
	}

	.header-wrapper {
		@include grid-mobile;
		@include centerH;
		align-items: center;
		margin-top: 25px;

		@media (min-width: $bp-3) {
			@include grid;
			margin-top: 120px;
		}
	}

	.title-container {
		@include centerH;
		display: flex;
		gap: 25px;
	}

	.menu {
		margin-left: 5px;
	}

	.controls {
		max-height: 45px;
		display: grid;
    row-gap: 5px;
    grid-template-columns: auto auto 1fr;
    grid-template-rows: auto;
    grid-template-areas:
      "one two empty"
      "three four four";
	}
</style>