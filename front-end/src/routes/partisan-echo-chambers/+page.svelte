<script lang="ts">
	// node_modules
    import { onMount } from "svelte";
    import { csv } from "d3-fetch";
    import { autoType } from "d3-dsv";
    import { group, extent } from "d3-array"
    import { scaleLinear } from 'd3-scale'

	// actions
	import inView from "$lib/actions/inView";

	// components
	import LineAreaChart from "$lib/components/graphs/LineAreaChart.svelte";
	import DoubleRangeSlider from "$lib/components/global/double-range-slider.svelte";
	import ControlSwitch from "$lib/components/global/control-switch.svelte";
	import ChartPlaceholder from '$lib/components/global/chart-placeholder.svelte';

	// // import utils
	import { formatMonth } from '$lib/utils/format-dates';

	import copy from '$lib/data/copy.json'
    const body: any[] = copy['partisan-echo-chambers']

	// prop declaration
	let loaded : boolean = false;

	// variable declaration
	let url : string = 'assets/data/EchoCh-nationwide-by_gender-or-age_group.csv'
	let data : any[]
	let dataIn : Map<any,any>
	let groupedData : any[]
	let xKey : string = 'date'
	let yKey : string = 'value'
	let zKey : number = 0
	let tvChecked : boolean = false;
	let tvChecked2 : boolean = false;
	let scenarioChecked : boolean = true;
	let scenarioChecked2 : boolean = true;
	let leanChecked : boolean = false;
	let leanChecked2 : boolean = true;
	let medium : string = tvChecked ? 'web' : 'tv'
	let partisanship_scenario : string = scenarioChecked ? 'stringent' : 'lenient'
	const scaleRange : Function = scaleLinear();
	let start = 0
	let end = 1
	let gender = 'All'
	let age_group = 'All'

	onMount(async () => {
		const res = await csv(url, autoType)
		data = res.map(d => ({ ...d, date: new Date(d.year, d.month, 1) }))

		const [ min, max ] = extent(data, d => +d.date); 
		scaleRange.range([ min, max ])
	})

	const scaleDate : Function = (x) => {
		const date = new Date(scaleRange(x))
		date.setDate(1)
		date.setHours(0, 0, 0)
		date.setMilliseconds(0)

		return +date
	}

	$: if (data) {
		dataIn = group(
			data, 
			d => d.gender, 
			d => d.medium, 
			d => d.partisanship_scenario,
			d => d.age_group,
			d => d.political_lean,
		)
	}

	$: if (data && dataIn.size) {
		groupedData = [
			...dataIn
				.get(gender)
				.get(medium)
				.get(partisanship_scenario)
				.get(age_group)
				.get(lean)
				.map(d => ({ ...d, idx: 0 })),
			...dataIn
				.get(gender2)
				.get(medium2)
				.get(partisanship_scenario2)
				.get(age_group2)
				.get(lean2)
				.map(d => ({ ...d, idx: 1 }))
		]
	}

	$: medium = tvChecked ? 'web' : 'tv'
	$: partisanship_scenario = scenarioChecked ? 'stringent' : 'lenient'
	$: gender = 'All'
	$: age_group = 'All'
	$: lean = leanChecked ? 'R' : 'L';

	$: medium2 = tvChecked2 ? 'web' : 'tv'
	$: partisanship_scenario2 = scenarioChecked2 ? 'stringent' : 'lenient'
	$: age_group2 = 'All'
	$: gender2 = 'All'
	$: lean2 = leanChecked2 ? 'R' : 'L';
</script>

<div class="section" use:inView={{ once: true }} on:enter={() => loaded = true }>
    {#each body as d, i}
	    {#if d.type === 'text'}
			<p class='copy'>
				{d.value}
			</p>
        {:else if d.type === 'title'} <h1 class='section-title'>{ d.value }</h1>
		{:else} 
			<div class='title-container'>
				<h3 class='chart-title'>
					{d.value.title}
				</h3>
			</div>
			
			<div class='controls-wrapper'>
				<div class='controls'>
					<ControlSwitch 
						id='political-lean' 
						title={'A lean'}
						labels={[ 'L', 'R' ]}
						colors={[ '#011f5b' , '#ff0000' ]}
						info={copy.controls.medium.description}
						bind:checked={ leanChecked } 
					/>
					<!-- title={copy.controls.medium.title} -->
					<ControlSwitch 
						id='medium' 
						title={copy.controls.medium.title}
						labels={[ 'TV', 'Web' ]}
						info={copy.controls.medium.description}
						bind:checked={ tvChecked } 
					/>
	
					<ControlSwitch 
						id='partisanship' 
						title={copy.controls.partisanship.title}
						labels={[ 
							copy.controls.partisanship['label-left'], 
							copy.controls.partisanship['label-right']
						]}
						info={copy.controls.partisanship.description}
						bind:checked={ scenarioChecked } 
					/>
	
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
	
				<div class='controls'>
					<ControlSwitch 
						id='political-lean' 
						title={'B lean'}
						labels={[ 'L', 'R' ]}
						colors={[ '#035aff' , '#990000' ]}
						info={copy.controls.medium.description}
						bind:checked={ leanChecked2 } 
					/>
					<!-- title={copy.controls.medium.title} -->
					<ControlSwitch 
						id='medium' 
						title={copy.controls.medium.title}
						labels={[ 'TV', 'Web' ]}
						info={copy.controls.medium.description}
						bind:checked={ tvChecked2 } 
					/>
	
					<ControlSwitch 
						id='partisanship' 
						title={copy.controls.partisanship.title}
						labels={[ 'Lenient', 'Strict' ]}
						info={copy.controls.partisanship.description}
						bind:checked={ scenarioChecked2 } 
					/>
	
					<div id='age-group' class='control control-menu'>
						<div class='control-title'>Age group</div>
						<select id="age-group-menu" name="age-group" bind:value={age_group2}>
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
						<select id="gender-menu" name="location" bind:value={gender2}>
							<option value='All' selected>All</option>
							<option value='Male'>Male</option>
							<option value='Female'>Female</option>
						</select>
					</div>
				</div>
				
				{#if loaded && data}
					<div id='period' class='control control-range'>
						<div class='control-title'>Period</div>
							<DoubleRangeSlider bind:start bind:end />
							<div class="labels">
								<div class="label">{ formatMonth(scaleRange(start)) }</div>
								<div class="label">{ formatMonth(scaleRange(end)) }</div>
							</div>
					</div>
				{/if}
	
				<div class='spacer'></div>
			</div>
			<div class='chart-wrapper'>
				{#if loaded && data}
					<LineAreaChart 
						data={ data }
						{ groupedData }
						scaleRange={ scaleDate }
						{ start }
						{ end }
						{ yKey } 
						{ xKey } 
						{ zKey }
						spanCol={12}
						customClass={'chart-medium'}
						formatTickX={formatMonth}
						url={ url }
						caption={d.value.captions}
					/>
					{:else} <ChartPlaceholder />
				{/if}
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

	.title-container {
		grid-column: span 12;
		margin-top: 25px;
	}

	.chart-wrapper {
        grid-column: 1 / span 12;
		margin-bottom: 25px;
    }

    .controls-wrapper {
        display: grid;
        grid-template-columns: 1fr auto 0.4fr;
        grid-template-rows: 1fr 1fr;
		margin-top: 25px;
        row-gap: 10px;
        column-gap: 5px;
		grid-column: 1 / span 12;

        .spacer {
            border-right: 1pt solid $light-grey;
            grid-row: 1 / span 2;
            grid-column: 2 / span 1;
        }
    }

    #period {
        grid-row: 1 / span 1;
        grid-column: 3 / span 1;
        padding-left: 25px;

        .control-title {
            width: 100%;
            @include fs-xxs;
            font-weight: 300;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .labels {
            flex-grow: 1;
            display: flex;
            justify-content: space-between;

            .label {
                @include fs-sm;
            }
        }
    }

    .controls {
        display: flex;
        grid-column: 1 / span 1;

        .control-switch, 
        .control-menu,
        .control-range {
            display: flex;
            // align-items: center;
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
</style>