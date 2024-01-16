<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { csv } from "d3-fetch";
  	import { autoType } from "d3-dsv";
	import { group, zip } from 'd3-array';

	// import state data
	import states from '../../data/states.json'
	import copy_data from '../../data/copy.json'

	// actions
	import inView from "../../actions/inView";

	// components
	import ChartPlaceholder from '../global/chart-placeholder.svelte';
	import ControlSwitch from "../global/control-switch.svelte";
	import StackedAreas from '../graphs/StackedAreas.svelte';

	// // import utils
	import { formatYear } from '../../utils/format-dates';
	import labelMap from '../../utils/labels';
	
	// prop declaration
	let loaded : boolean = false;
	export let once : boolean;
	export let body : any[];
    export let refs : any[];
    export let chart : any;
	export let title : any;
	export let modal : any;

	// chart config
	let data : any[];
	let dataMap : Map<string, any>
	let rows : number[]
	let tvChecked : boolean = false;
	const urlChart : string  = 'assets/data/EchoCh-national_consumption_tv_and_web.csv'
	
	onMount(async () => {
		// load data for map + line chart
		const resChart = await csv(urlChart, autoType)
		data = resChart
			.map(d => ({ ...d, date: new Date(d.year, d.month, 1) }))
			.sort((a, b) => +a.date - +b.date)
    	// parse data for 
		dataMap = group(
			data,
			d => d.medium,
			d => d.gender,
			d => d.age_group,
			d => d.state,
			d => +d.date,
			d => d.category
		)

		rows = Array.from(new Set(data.map(d => +d.date)))
	})

	const chartConfig : Map<string, { order : string[], colors: string[] }> = new Map([
		['tv', {
			order: ['non-news', 'news'],
			colors: ['#a6cee3', '#fb9a99'],
			yDomain: [0, 350]
		}
		],
		['web', {
			order: ['non_news', 'facebook', 'hard_news', 'youtube', 'twitter', 'reddit', 'fake_news'],
			colors: ['#a6cee3',  '#e31a1c', '#fb9a99', '#cab2d6', '#fdbf6f', '#ff7f00', '#6a3d9a'],
			yDomain: [0, 80]
		}],
	])

	$: medium = tvChecked ? 'web' : 'tv'
	$: gender = 'All'
    $: age_group = 'All'
	$: location = 'US'
	$: activeChart = chartConfig.get(medium)

	function resetAge() { age_group = 'All' }
    function resetGender() { gender = 'All' }
	function resetState() { location = 'US' }

	$: if (location !== 'US') { resetGender(); resetAge(); }
	$: if (age_group !== 'All' || gender !== 'All') { resetState() }
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
			
				<div class='controls'>
					<ControlSwitch 
						id='medium' 
						title={copy_data.controls.medium.title}
						labels={[ 
							copy_data.controls.medium['label-left'], 
							copy_data.controls.medium['label-right']
						]}
						info={copy_data.controls.medium.description}
						bind:checked={ tvChecked } 
					/>
			
					<div id='location' class='control control-menu'>
						<div class='control-title'>Location</div>
						<select id="age-group-menu" name="location" bind:value={location}>
							<option value={'US'}>US</option>
							{#each states.sort((a,b) => a.state.localeCompare(b.state)) as state}
								<option value={state.abbr}>{state.state}</option>
							{/each}
						</select>
					</div>
			
					<div id='age-group' class='control control-menu'>
						<div class='control-title'>Age group</div>
						<select id="age-group-menu" name="age-group" bind:value={age_group}>
							<option value='All'>All</option>
							<option value='18-24'>18-24</option>
							<option value='25-34'>25-34</option>
							<option value='35-44'>35-44</option>
							<option value='45-54'>45-54</option>
							<option value='55+'>55+</option>
						</select>
					</div>
			
					<div id='gender' class='control control-menu'>
						<div class='control-title'>Gender</div>
						<select id="gender-menu" name="location" bind:value={gender}>
							<option value='All' selected>All</option>
							<option value='Male'>Male</option>
							<option value='Female'>Female</option>
						</select>
					</div>
				</div>
			
				<div class='legend'>
					{#each zip(activeChart.colors, activeChart.order) as cat}
						<div class='legend-item'>
							<div class={'legend-color'} style='--color: {cat[0]}'></div>
							<div>{labelMap.get(cat[1])}</div>
						</div>
					{/each}
				</div>
			
				{#if data}
					<StackedAreas 
						dataMap={dataMap.get(medium).get(gender).get(age_group).get(location)} 
						{data} 
						{rows} 
						categories={activeChart.order} 
						colors={activeChart.colors}
						yDomain={activeChart.yDomain}
						formatter={formatYear}
						caption={chart.captions}
						url={ urlChart }
					/>
					
					{:else} <ChartPlaceholder />
				{/if}
			</div>
		{/if}
	{/each}
	<div 
		class='close-button bottom' 
		on:click={() => modal = false }
	>
		GO BACK
	</div>
</div>

<style lang='scss'>
	.section {
        grid-template-columns: repeat(12, 1fr);
        column-gap: 0;

        @media (min-width: $bp-3) {
            column-gap: 50px;
        }
    }

	.section-title {
        border-bottom: 0.5pt solid black;
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

		h3 {
			margin-bottom: 1em;
		}
	}

	.controls {
        display: flex;

        .control-switch, 
        .control-menu,
        .control-range {
            display: flex;
            flex-wrap: wrap;
        
            .control-title {
                width: 100%;
                @include fs-xxs;
                font-weight: 300;
                letter-spacing: 1px;
                text-transform: uppercase;

                .info {
                background-color: $off-white;
                display: inline-block;
                width: 12px;
                border-radius: 100%;
                text-align: center;
                @include fs-xs;
                }
            }

            .control-label {
                @include fs-sm;
            }
            .control-label.active {
                text-decoration: underline;
            }

            select {
                margin: 0;
                @include fs-sm;
            }
        }
	}

	.legend {
		display: flex; 
		gap: 15px;
		margin-top: 15px;
		font-size: 14px;

		.legend-item {
			display: flex;
			align-items: center;
			gap: 5px;
			
			.legend-color {
				background-color: var(--color);
				width: 17.5px;
				height: 17.5px;
				border-radius: 3px;
			}
		}
	}

	.close-button.bottom {
		grid-column: 6 / span 2;
		text-align: center;
		cursor: pointer;
        @include fs-sm;
	}

	.close-button:hover {
        opacity: 0.85;
    }

    .close-button:after {
        content: '\2715';
        line-height: 1;
        margin-left: 5px;
    }
</style>
