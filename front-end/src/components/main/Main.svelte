<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { flatten } from 'layercake';
	import { csv } from "d3-fetch";
  	import { autoType } from "d3-dsv";
	import { group, zip } from 'd3-array';

	// types
	import type Author from '../../types/Authors';

	// import state data
	import states from '../../data/states.json'
	import copy_data from '../../data/copy.json'

	// components
	import Title from '../copy/Title.svelte';
	import Description from '../copy/Description.svelte';
	import Authors from '../copy/Authors.svelte';
	import ChartPlaceholder from '../global/chart-placeholder.svelte';
	import ControlSwitch from "../global/control-switch.svelte";
	import StackedAreas from '../graphs/StackedAreas.svelte';

	// // import utils
	import { formatYear } from '../../utils/format-dates';
	import labelMap from '../../utils/labels';
	
	// prop declaration
	export let title : string;
	export let standfirst : any[] = [{value: 'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Commodi consequatur inventore exercitationem ex perferendis provident, earum cumque maiores quam quidem labore, mollitia odit eaque laborum?'}]
	export let authors : Author[];
	export let captions : any[]

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
			colors: ['#33a02c', '#b2df8a'],
			yDomain: [0, 350]
		}
		],
		['web', {
			order: ['non_news', 'facebook', 'hard_news', 'youtube', 'twitter', 'reddit', 'fake_news'],
			colors: ['#a6cee3',  '#e31a1c', '#fb9a99', '#cab2d6', '#fdbf6f', '#ff7f00', '#6a3d9a'],
			yDomain: [0, 100]
		}],
	])
	
	// $: politicalChecked = true
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

<main>
	<div class='header-wrapper main-column'>
		<Title title={ title }></Title>
		<Description standfirst={ standfirst }></Description>
		<Authors authors={ authors }></Authors>
	</div>

	<div class='chart-wrapper'>
        <div class='controls'>
            <ControlSwitch 
                id='medium' 
                title={copy_data.controls.medium.title}
                labels={[ 'TV', 'Web' ]}
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
				caption={captions[0].value}
				url={ urlChart }
			/>
			
			{:else} <ChartPlaceholder row={0}/>
		{/if}
	</div>
	
	
</main>

<style lang='scss'>
	main {
		max-width: $column-width;
		margin: 0 auto;
	}

	.header-wrapper {
		@include grid-mobile;
		@include centerH;
		align-items: center;
		margin: 25px 0;

		@media (min-width: $bp-3) {
			@include grid-main;
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
		gap: 10px;
		margin-top: 15px;

		.legend-item {
			display: flex;
			align-items: center;
			gap: 3px;
			
			.legend-color {
				background-color: var(--color);
				width: 15px;
				height: 15px;
			}
		}
	}
</style>