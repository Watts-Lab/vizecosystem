<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { csv } from "d3-fetch";
  	import { autoType } from "d3-dsv";
	import { group, extent, zip } from 'd3-array';

	// import state data
	import states from '$lib/data/states.json'
	import copy from '$lib/data/copy.json'
    const body: any[] = copy['overall-news-consumption']

	// actions
	import inView from "$lib/actions/inView";

	// components
	import ChartPlaceholder from '$lib/components/global/chart-placeholder.svelte';
	import ControlSwitch from "$lib/components/global/control-switch.svelte";
	import SelectMenu from '$lib/components/global/select-menu.svelte';
	import StackedAreas from '$lib/components/graphs/StackedAreas.svelte';
	import Caption from '$lib/components/graphs/layers/Caption.svelte';

	// // import utils
	import { formatYear } from '$lib/utils/format-dates';
	import labelMap from '$lib/utils/labels';
	
	// prop declaration
	let loaded : boolean = false;

	// chart config
	let data : any[];
	let dataMap : Map<string, any>
	let rows : number[]
	let xTicks : Date[]
	let xDomain : Date[]
	let axisChecked : boolean = true;
	const urlChart : string  = 'assets/data/EchoCh-national_consumption_tv_and_web.csv'
	
	onMount(async () => {
		// load data for map + line chart
		const resChart = await csv(urlChart, autoType)
		data = resChart
			.map((d: any) => ({ ...d, date: new Date(d.year, d.month, 1) }))
			.sort((a: any, b: any) => +a.date - +b.date)
    	// parse data for 
		dataMap = group(
			data,
			(d: any) => d.medium,
			(d: any) => d.gender,
			(d: any) => d.age_group,
			(d: any) => d.race,
			(d: any) => d.state,
			(d: any) => +d.date,
			(d: any) => d.category
		)

		rows = Array.from(new Set(data.map((d: any) => +d.date)))
		xTicks = Array.from(new Set(data.map(d => d.year))).map(d => new Date(d, 0, 1))
		xDomain = extent(data, (d: any) => d.date)
	})

	const chartConfig : Map<string, { order : string[], colors: string[], yDomain: number[] }> = new Map([
		['tv', {
			order: ['non-news', 'news'],
			colors: ['#a6cee3', '#fb9a99'],
			yDomain: [0, 350]
		}
		],
		['web', {
			order: ['non_news', 'hard_news', 'fake_news', 'social_media'],
			colors: ['#a6cee3',  '#fb9a99', '#e31a1c', '#fdbf6f'],
			yDomain: [0, 100]
		}],
		['mobile', {
			order: ['music', 'news', 'other', 'social_media'],
			colors: ['#17A589',  '#fb9a99', '#a6cee3', '#fdbf6f' ],
			yDomain: [0, 60]
		}],
	])

	$: syncAxis = axisChecked === true
	$: gender = 'All'
    $: age_group = 'All'
	$: ethnicity = 'All'
	$: location = 'US'
	$: disableMenus = location !== 'US'

	function resetAge() { age_group = 'All' }
    function resetGender() { gender = 'All' }
	function resetEthnicity() { ethnicity = 'All' }
	function resetState() { location = 'US' }

	$: if (location !== 'US') { resetGender(); resetAge(); resetEthnicity(); }
	$: if (age_group !== 'All' || gender !== 'All') { resetState() }
	$: disableAgeGroup = ethnicity !== 'All' && gender !== 'All'
	$: disableGender = age_group !== 'All' && ethnicity !== 'All'
	$: disableEthnicity = age_group !== 'All' && gender !== 'All'
	
	//@ts-ignore
	$: stateMap = new Map<string,string>([
		['US', 'US'],
		...states.sort((a,b) => a.state.localeCompare(b.state)).map((d: any) => [d.abbr, d.state])
	])

	$: ethnicityMap =  new Map([
		['All', 'All'],
		['white+other', 'White/Other'],
		['black', 'Black'],
		['hispanic', 'Hispanic'],
		['asian', 'Asian'],
	])
</script>

<div class="section" use:inView={{ once: true }} on:enter={() => loaded = true }>
	{#each body as d, i}
		{#if d.type === 'text'}
			<p class='copy'>
				{d.value}
			</p>
        {:else if d.type === 'title'} <h1 class='section-title'>{ d.value }</h1>
		{:else}
			<div class='chart-container'>
				<h3 class='chart-title'>
					{d.value.title}
				</h3>
			
				<div class='controls'>
					<SelectMenu 
						id='location' 
						title={'Location'}
						options={stateMap}
						bind:value={location}
					/>
								
					<SelectMenu 
						id='age-group' 
						title={'Age group'}
						options={new Map([
							['All', 'All'],
							['18-24', '18-24'],
							['25-34', '25-34'],
							['35-44', '35-44'],
							['45-54', '45-54'],
							['55+', '55+']	
						])}
						disabled={disableMenus || disableAgeGroup}
						bind:value={age_group}
					/>

					<SelectMenu 
						id='gender' 
						title={'Gender'}
						options={new Map([
							['All', 'All'],
							['Male', 'Male'],
							['Female', 'Female']
						])}
						disabled={disableMenus || disableGender}
						bind:value={gender}
					/>

					<SelectMenu 
						id='ethnicity' 
						title={'Ethnicity'}
						options={ethnicityMap}
						disabled={disableMenus || disableEthnicity}
						bind:value={ethnicity}
					/>

					<ControlSwitch 
						id='axis' 
						title={'Independent axis'}
						labels={[ 
							'Independent',
							'Aligned'
						]}
						info={'The axis bla bla bla'}
						bind:checked={ axisChecked } 
					/>
				</div>
			
				<div class='legend'>
					{#each zip(
						[...chartConfig.get('tv').colors, ...chartConfig.get('web').colors, ...chartConfig.get('mobile').colors], 
						[...chartConfig.get('tv').order, ...chartConfig.get('web').order, ...chartConfig.get('mobile').order]
					) as cat}
						<div class='legend-item'>
							<div class={'legend-color'} style='--color: {cat[0]}'></div>
							<div>{labelMap.get(cat[1])}</div>
						</div>
					{/each}
				</div>
			
				{#if data}
					<div class='chart-grid'>
						<div class='chart-inner'>
							<h4>TV</h4>
							<StackedAreas 
								dataMap={
									dataMap
									.get('tv')
									.get(gender)
									.get(age_group)
									.get(ethnicity)
									.get(location)
								}
								{data} 
								{rows} 
								categories={chartConfig.get('tv').order} 
								colors={chartConfig.get('tv').colors}
								yDomain={chartConfig.get('tv').yDomain}
								{xDomain}
								{xTicks}
								formatter={formatYear}
								includeCaption={false}
								url={ urlChart }
							/>
						</div>

						<div class='chart-inner'>
							<h4>Desktop</h4>
							<StackedAreas 
								dataMap={
									dataMap
										.get('web')
										.get(gender)
										.get(age_group)
										.get(ethnicity)
										.get(location)
								}
								{data} 
								{rows} 
								categories={chartConfig.get('web').order} 
								colors={chartConfig.get('web').colors}
								yDomain={chartConfig.get(syncAxis ? 'tv': 'web').yDomain}
								{xDomain}
								{xTicks}
								addTickYLabel={false}
								formatter={formatYear}
								includeCaption={false}
								url={ urlChart }
							/>
						</div>

						<div class='chart-inner'>
							<h4>Mobile</h4>
							<StackedAreas 
								dataMap={
									dataMap
										.get('mobile')
										.get(gender)
										.get(age_group)
										.get(ethnicity)
										.get(location)
								}
								{data} 
								{rows} 
								categories={chartConfig.get('mobile').order} 
								colors={chartConfig.get('mobile').colors}
								yDomain={chartConfig.get(syncAxis ? 'tv': 'mobile').yDomain}
								{xDomain}
								{xTicks}
								addTickYLabel={false}
								formatter={formatYear}
								includeCaption={false}
								url={ urlChart }
							/>
						</div>
					</div>
					{:else} <ChartPlaceholder />
				{/if}

				<Caption caption={ d.value.captions } url={ urlChart } type={'single-cols'} />
			</div>
		{/if}
	{/each}
</div>

<style lang='scss'>
	.section {
        grid-template-columns: repeat(12, 1fr);
        column-gap: 15px;

    }

	.section-title {
        @include fs-xl;
        grid-row: 1 / span 1;
        grid-column: 3 / span 8;
        margin-bottom: 1em;
    }

	.copy {
        grid-column: span 12;

        @media (min-width: $bp-3) {
            grid-column: 3 / span 8;
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

	.chart-container {
		grid-column: span 12;
        margin: 25px 0;

		h3 {
			margin-bottom: 1em;
		}

		.chart-grid {
			display: grid;
			column-gap: 15px;
			grid-template-columns: repeat(3, 1fr);

			.chart-inner {
				display: grid;

				h4 {
					margin: 15px 0 10px 0;
				}
			}
		}
	}

	.controls {
        display: flex;

        .control-switch, 
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
		margin: 15px 0;
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
</style>
