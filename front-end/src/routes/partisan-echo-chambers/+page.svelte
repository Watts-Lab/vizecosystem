<script lang="ts">
	// node_modules
    import { onMount } from "svelte";
	import { fade } from "svelte/transition";
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
	import SelectMenu from '$lib/components/global/select-menu.svelte';
	import ChartPlaceholder from '$lib/components/global/chart-placeholder.svelte';

	// // import utils
	import { formatMonth } from '$lib/utils/format-dates';
	import parseCopy from '$lib/utils/parse-copy';
	import milestones from "$lib/utils/milestones";

	import copy from '$lib/data/copy.json'
    const body: any[] = copy['partisan-echo-chambers']

	// prop declaration
	let loaded : boolean = false;

	// variable declaration
	let url : string = 'assets/data/EchoCh-nationwide-by_gender-age-race.csv'
	let data : any[]
	let dataIn : Map<any,any>
	let groupedData : any[]
	let xKey : string = 'date'
	let yKey : string = 'value'
	let zKey : number = 0
	let scenarioChecked : boolean = false;
	let partisanship_scenario : string = scenarioChecked ? 'stringent' : 'lenient'
	const scaleRange : Function = scaleLinear();
	let start = 0
	let end = 1
	let gender = 'All'
	let age_group = 'All'

	onMount(async () => {
		const res = await csv(url, autoType)
		data = res.map(d => ({ ...d, date: new Date(d.year, d.month - 1, 1) }))

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
			(d: any) => d.partisanship_scenario,
			(d: any) => d.gender,
			(d: any) => d.age_group,
			(d: any) => d.ethnicity,
			(d: any) => d.political_lean,
			(d: any) => d.medium,
			(d: any) => d.diet_threshold,
		)
	}

	$: if (data && dataIn.size) {
		groupedData = dataIn
			.get(partisanship_scenario)
			.get(gender)
			.get(age_group)
			.get(ethnicity)
	}

	$: partisanship_scenario = scenarioChecked ? 'stringent' : 'lenient'
	$: gender = 'All'
	$: age_group = 'All'
	$: ethnicity = 'All'
	$: userInteractedWithControls = false;

	$: disableAgeGroup = ethnicity !== 'All' && gender !== 'All'
	$: disableGender = age_group !== 'All' && ethnicity !== 'All'
	$: disableEthnicity = age_group !== 'All' && gender !== 'All'
	$: if ((disableAgeGroup || disableGender || disableEthnicity)) {
		userHasReachedLastLevel = true;
		renderReachedLastLevelLabel = true;
		setTimeout(() => renderReachedLastLevelLabel = false, 5000);
	}

	$: userHasReachedLastLevel = false
	$: renderReachedLastLevelLabel = false;
</script>

<div class="section" use:inView={{ once: true }} on:enter={() => loaded = true }>
    {#each body as d, i}
	    {#if d.type === 'text'}
			<p class='copy'>
				{@html parseCopy(d.value)}
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
						id='partisanship' 
						title={copy.controls.partisanship.title}
						labels={[ 
							copy.controls.partisanship['label-left'], 
							copy.controls.partisanship['label-right']
						]}
						info={copy.controls.partisanship.description}
						bind:checked={ scenarioChecked } 
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
						disabled={disableAgeGroup}
						bind:value={age_group}
						bind:userInteractedWithControls
					/>
	
					<SelectMenu 
						id='gender' 
						title={'Gender'}
						options={new Map([
							['All', 'All'],
							['Male', 'Male'],
							['Female', 'Female']
						])}
						disabled={disableGender}
						bind:value={gender}
						bind:userInteractedWithControls
					/>

					<SelectMenu 
						id='ethnicity' 
						title={'ethnicity'}
						options={new Map([
							['All', 'All'],
							['white+other', 'White/Other'],
							['black', 'Black'],
							['hispanic', 'Hispanic'],
							['asian', 'Asian'],
						])}
						disabled={disableEthnicity}
						bind:value={ethnicity}
						bind:userInteractedWithControls
					/>

					{#if userHasReachedLastLevel && renderReachedLastLevelLabel}
						<p 
							class='warning'
							in:fade
						>No further breakdown available</p>
					{/if}
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
	
				<!-- <div class='spacer'></div> -->
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
						displayAnnotation={ false }
						{ milestones }
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
        grid-template-rows: 1fr;
		margin: 25px 0;
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
		position: relative;

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

		.warning {
			position: absolute;
			color: $css-lab-dark-red;
			top: -15px;
			left: 212px;
			@include fs-xs;
		}
    }
</style>