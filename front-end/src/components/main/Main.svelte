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
	import Beeswarm from '../graphs/Beeswarm.svelte';
	import ChartPlaceholder from '../global/chart-placeholder.svelte';

	// prop declaration
	export let title : string;
	export let standfirst : any[] = [{value: 'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Commodi consequatur inventore exercitationem ex perferendis provident, earum cumque maiores quam quidem labore, mollitia odit eaque laborum?'}]
	export let authors : Author[];

	// local data
	import states from '../../data/states_centroids.json'

	// chart config
	
	let data : any[];
	let dataMap : Map<string, any>
  let fullDataMap : Map<string, any>
	const url : string  = 'assets/data/dupe-data-by-state-grid-map.csv'
	
	onMount(async () => {
		const res = await csv(url, autoType)
		data = res
    // parse data for 
		dataMap = group(
			res.filter(d => d.month === 4),
			d => d.state,
      // d => d.political_lean,
			d => d.medium, 
			d => d.diet_threshold,
			d => d.partisanship_scenario
		)
    fullDataMap = group(
			res.filter(d => d.month === 4),
			d => d.state, 
			d => d.diet_threshold,
			d => d.partisanship_scenario
		)
	})

	const chartConfig : Map<number,ChartConfig> = new Map([
		[0, {
			type: "diverging",
			rScale: scaleSqrt,
			rDomain: [0, 20],
			rRange: [3, 150],
			zScale: scaleThreshold,
			zDomain: [-0.75, -0.5, -0.1, 0.1, 0.5, 0.75],
			colorInterpolator: scaleDiverging,
			colorInterpolatorDomain: [-1, 0, 1],
			colorInterpolatorScheme: ["#011f5b", "gainsboro", "#990000"],
			colorPaletteAnchors: [-0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75]
		}],
		[1, {
			type: "linear",
			rScale: scaleSqrt,
			rDomain: [0, 20],
			rRange: [3, 150],
			zScale: scaleThreshold,
			zDomain: [0, 0.25, 0.5, 1],
			colorInterpolator: scaleLinear,
			colorInterpolatorDomain: [0, 1],
			colorInterpolatorScheme: "gainsboro",
			colorPaletteAnchors: [0, 0.25, 0.5, 0.75, 1]
		}],
	])

	$: chart = "0"
	$: activeChart = chartConfig.get(+chart)
</script>

<main>
	<div class='header-wrapper main-column'>
		<Title title={ title }></Title>
		<Description standfirst={ standfirst }></Description>
		<Authors authors={ authors }></Authors>
	</div>
	
	<div class='title-container main-column'>
			<h3 class='chart-title'>
				My chart title 
				<select bind:value={chart}>
					<option value="0">Chart 1</option>
					<option value="1">Chart 2</option>
				</select>
			</h3>
	</div>
	{#if data && data.length}
		<Beeswarm
			{ data }
			{ states }
			{ dataMap }
      { fullDataMap }
			{ activeChart }
		/>
		{:else} <ChartPlaceholder />
	{/if}
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
	}

</style>