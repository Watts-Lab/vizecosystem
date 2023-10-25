<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { csv } from "d3-fetch";
  	import { autoType } from "d3-dsv";
	import { group, rollup, descending, rank } from 'd3-array';
	import { scaleDiverging, scaleThreshold, scaleSqrt } from 'd3-scale';

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
	export let body : any[]
    export let refs : any[]
    export let captions : any[]
	export let title : any;

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
		const rankVars : string[] = ['left_pct', 'right_pct', 'left_size', 'right_size']
		const ranks = rollup(
			resChart, 
			v => {
				const varObj = {}
				rankVars.forEach(r => {
					const statesObj = {}
					const ranked = rank(v.map(d => d[r]), descending)
					v.forEach((d, i)=> { statesObj[d.state] = ranked[i] + 1 })
					varObj[r] = statesObj
				})

				return varObj
			}, 
			d => d.period, 
			d => d.medium, 
			d => d.diet_threshold, 
			d => d.partisanship_scenario
		)
		data = resChart.map(d => ({ 
			...d,
			left_pct_rk: ranks.get(d.period).get(d.medium).get(d.diet_threshold).get(d.partisanship_scenario)['left_pct'][d.state],
			right_pct_rk: ranks.get(d.period).get(d.medium).get(d.diet_threshold).get(d.partisanship_scenario)['right_pct'][d.state],
			left_size_rk: ranks.get(d.period).get(d.medium).get(d.diet_threshold).get(d.partisanship_scenario)['left_size'][d.state],
			right_size_rk: ranks.get(d.period).get(d.medium).get(d.diet_threshold).get(d.partisanship_scenario)['right_size'][d.state]
		}))

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
	])

	$: chart = "0"
	$: activeChart = chartConfig.get(+chart)
	$: politicalChecked = true
</script>

<div class="section" use:inView={{ once }} on:enter={() => loaded = true }>
	<h1 class='section-title'>{ title.value }</h1>
        {#each body as d, i}
			{#if d.type === 'text'}
				<p class='copy'>
					{d.value}
				</p>
			{:else}
				<div class='title-container'>
					<h3 class='chart-title'>
						{d.value.title}
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
						caption={ captions[0].value }
						tooltipCaptions={ captions.slice(1) }
						url={ urlChart }
					/>
					{:else} <ChartPlaceholder row={5} />
				{/if}
			{/if}
        {/each}
</div>

<style lang='scss'>
	section {
        grid-template-columns: repeat(12, 1fr);
        column-gap: 0;

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
        grid-row: 1 / span 1;
        grid-column: span 12;
		margin-bottom: 1em;
    }

    .copy {
        grid-column: span 12;

        @media (min-width: $bp-3) {
            grid-column: 1 / span 7;
        }
    }

	p {
		margin-top: 0;
		margin-bottom: 1em;
		@include fs-root;

		@media (min-width: $bp-3) {
			@include fs-md;
		}
	}

	.title-container {
		grid-column: span 12;
	}
</style>