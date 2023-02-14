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
	import ControlSwitch from '../global/control-switch.svelte';

	// prop declaration
	export let title : string;
	export let standfirst : any[] = [{value: 'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Commodi consequatur inventore exercitationem ex perferendis provident, earum cumque maiores quam quidem labore, mollitia odit eaque laborum?'}]
	export let authors : Author[];

	// local data
	import states from '../../data/states_centroids.json'

	// chart config
	
	let data : any[];
	let table : any[];
	let dataMap : Map<string, any>
  let fullDataMap : Map<string, any>
	let tableMap : Map<string|number, any>
	const urlChart : string  = 'assets/data/dupe-data-by-state-grid-map.csv'
	const urlTable : string  = 'assets/data/dupe-data-by-state-PROGRAMS.csv'
	
	onMount(async () => {
		// load data for map + line chart
		const resChart = await csv(urlChart, autoType)
		data = resChart.map(d => ({ ...d, date: new Date(d.year, d.month, 1) }))
    // parse data for 
		dataMap = group(
			data,
			d => +d.date,
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

		// load data for tables
		// load data for map + line chart
		const resTable = await csv(urlTable, autoType)
		table = resTable.map(d => ({ ...d, date: new Date(d.year, d.month, 1) }))
		tableMap = group(
			table,
			d => +d.date,
			d => d.state,
			d => d.medium,
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
	$: politicalChecked = true
</script>

<main>
	<div class='header-wrapper main-column'>
		<Title title={ title }></Title>
		<Description standfirst={ standfirst }></Description>
		<Authors authors={ authors }></Authors>
	</div>
	
	<div class='title-container main-column'>
			<h3 class='chart-title'>
				Partisan Segregation in the US:
				<select class='menu' bind:value={chart}>
					<option value="0">Comparison view</option>
					<option value="1">Single political lean view</option>
				</select>
			</h3>

			{#if activeChart.type === 'linear'}
				<div class='controls'>
					<ControlSwitch 
						id='medium' 
						title='Political lean'
						labels={[ 'R', 'L' ]}
						info='Right or left leaning'
						colors={[ "#AA3737", "#384E83" ]}
						bind:checked={ politicalChecked } 
					/>
				</div>
			{/if}
	</div>


	
	{#if (data && data.length) && (table && table.length)}
		<Beeswarm
			{ data }
			{ states }
			{ dataMap }
      { fullDataMap }
			{ tableMap }
			{ activeChart }
			{ politicalChecked }
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