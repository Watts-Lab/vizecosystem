<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { csv } from "d3-fetch";
  import { autoType } from "d3-dsv";
	import { group } from 'd3-array';
	import { scaleDiverging, scaleThreshold, scaleSqrt, scaleLinear } from 'd3-scale';

	// types
	import type ChartConfig from '../../types/ChartConfig';

	// actions
	import inView from "../../actions/inView";

	// components
	import Beeswarm from '../graphs/Beeswarm.svelte';
	import ChartPlaceholder from '../global/chart-placeholder.svelte';
	import ControlSwitch from '../global/control-switch.svelte';

	// prop declaration
	let loaded : boolean = false;
	export let once : boolean;
	export let copy : any[]
    export let refs : any[]
    export let captions : any[]

	// local data
	import states from '../../data/states_centroids.json'

	// chart config
	let data : any[];
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
			rRange: [8, 80],
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
			rRange: [8, 80],
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

<div class="section section-1" use:inView={{ once }} on:enter={() => loaded = true }>
	<h1 class='section-title'>Section title</h1>
    <div class='copy'>
        {#each copy as d, i}
            <p>
                {d.value}
            </p>
        {/each}
    </div>

	<div class='title-container'>
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
						labels={[ 'L', 'R' ]}
						info='Right or left leaning'
						colors={[ "#AA3737", "#384E83" ]}
						bind:checked={ politicalChecked } 
					/>
				</div>
			{/if}
	</div>
	
	{#if loaded && (data && data.length)}
		<Beeswarm
			{ data }
			{ states }
			{ dataMap }
			{ fullDataMap }
			{ activeChart }
			{ politicalChecked }
		/>
		{:else} <ChartPlaceholder row={5}/>
	{/if}
</div>

<style lang='scss'>
	.section-1 {
        grid-template-columns: repeat(12, 1fr);
        column-gap: 0;
        grid-template-rows: auto auto auto auto auto;

        @media (min-width: $bp-3) {
            column-gap: 50px;
        }
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

	.section-title {
        border-bottom: 1pt solid black;
        // margin: 0 0 25px 0;
        grid-row: 1 / span 1;
        grid-column: span 12;
    }

    .copy {
        grid-row: 2 / span 1;
        grid-column: span 12;

        @media (min-width: $bp-3) {
            grid-column: span 7;
        }
    }

	.title-container {
		grid-row: 3 / span 1;
		grid-column: span 12;
	}
</style>