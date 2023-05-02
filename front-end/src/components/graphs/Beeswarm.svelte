<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { LayerCake, Svg, Html } from 'layercake';
	import { piecewise, interpolateRgb } from 'd3-interpolate';
	import { timeFormat } from 'd3-time-format';

	// types
	import type ChartConfig from '../../types/ChartConfig';

	// components
	// import Force from './Force_2.svelte';
	import ForceDiverging from './ForceDiverging.svelte';
	import ForceLinear from './ForceLinear.svelte';
	import PopupOverlay from './tooltips/PopupOverlay.svelte';
	import ControlSwitch from '../global/control-switch.svelte';
	// import HowTo from './archive/HowTo.svelte'

	// // utils
	
	// local data
	import statesDict from '../../data/states.json'

	const statesMap = new Map(statesDict.map(d => [d.state, d]))

	// props declaration
	export let data : any[];
	export let states : any[];
	export let dataMap : Map<string|number, any>
	export let fullDataMap : Map<string|number, any>
	export let activeChart : ChartConfig;

	// variable declaration
	let colorInterpolator : any;
	export let politicalChecked : boolean;
	let dietChecked : boolean = true;
  let scenarioChecked : boolean = true;
	let tvChecked : boolean = true
	$: political_lean = politicalChecked ? 'R' : 'L'
	$: medium = tvChecked ? 'web' : 'tv';
	$: diet_threshold = dietChecked ? 75 : 50;
  $: partisanship_scenario = scenarioChecked ? 'lenient' : 'stringent';

	// tooltip togglers
	$: tooltip = null;
	let hideTooltip : boolean = true;
	// overlay pop up togglers
	$: popup = null;
	let hidePopup : boolean = true;
	// other global vars
	let render : boolean = false;
	let dataIn : any;

	// when component is rendered, set render to true
	// this will allow the inner contents of the LayerCake
	// component to render after width/height has been set
	onMount(() => {
		render = true
	})
	
	// event handlers
	function handleMouseEnter(e : CustomEvent<any>) { 
		hideTooltip = false;
		tooltip = e;
	}

	function handleMouseLeave() {
		hideTooltip = true;
		tooltip = null;
	}

	function handleClick(e : CustomEvent<any>) {
		hidePopup = false;
		popup = e;
	}

	function handleClosePopup() {
		hidePopup = true;
		popup = null;
	}

	const dates = [ ...new Set(data.map(d => d.period)) ]
	let initPeriod = 'Last month'
	let period = initPeriod
	
	$: dataIn = states
		.map(d => {
			const { abbr } = statesMap.get(d.state)
			const data = dataMap
				.get(period || initPeriod)
				.get(abbr)
				.get(medium)
				.get(diet_threshold)
				.get(partisanship_scenario)[0]
			return { ...d, abbr, data  }
		})

	$: rScale = activeChart.rScale()
		.domain(activeChart.rDomain)
		.range(activeChart.rRange);

	$: {
		colorInterpolator = activeChart.colorInterpolator()
			.domain(activeChart.colorInterpolatorDomain)
		
		if (activeChart.type === 'diverging') {
			colorInterpolator.interpolator(piecewise(
				interpolateRgb.gamma(0.5),
				activeChart.colorInterpolatorScheme
			))
		}
		else if (activeChart.type === 'linear') {
			colorInterpolator.range([
				activeChart.colorInterpolatorScheme, 
				political_lean === 'R' ? '#990000' : "#011f5b"
			])
		}
	}

	$: colorPalette = activeChart.colorPaletteAnchors.map(colorInterpolator)

	$: zScale = activeChart.zScale()
		.domain(activeChart.zDomain)
		.range(colorPalette)
</script>

<div class='chart-info-wrapper main-column'>
	<div class='controls'>
		<ControlSwitch 
			id='medium' 
			title='Medium'
			labels={[ 'TV', 'Web' ]}
			info='Internet or TV'
			bind:checked={ tvChecked } 
		/>

		<!-- inverting labels manually for now -->
		<ControlSwitch 
			id='partisanship' 
			title='Partisanship'
			labels={[ 'Stringent', 'Lenient' ]} 
			info='Lenient means that websites more partisan than TheGuardian.com (FoxNews.com) are counted as left (right), and CNN is counted as left-leaning. The stric definition means partisan content bounds are Slate.com (Breitbart.com) on the left (right)'
			bind:checked={ scenarioChecked } 
		/>

		<ControlSwitch 
			id='diet' 
			title='Diet %'
			labels={[ '50%', '75%' ]}
			info='Percent of intra-individual news diets that must be partisan for partisan segregation'
			bind:checked={ dietChecked } 
		/>

		<div id='period' class='control control-menu'>
			<div class='control-title'>Period</div>
			<select id="period-menu" name="period" bind:value={period}>
				{#each dates as date, i}
					<option value={date}>
						{date}
					</option>
				{/each}
			</select>
		</div>
	</div>

	<div class='legend'>
		<div class='legend-item legend-item-color'>
			<h5>Partisan lean</h5>
			{#if activeChart.type !== 'linear'}
				<span>More left</span>
			{/if}
			{#each colorPalette as d}
				<div class='legend-block' style="--color: {d}"></div>
			{/each}
			<span>More { political_lean === 'L' ? 'left' : 'right' }</span>
		</div>
		
		<div class='legend-item legend-item-size'>
			<h5>How to read this chart?</h5>
			<div>
				<!-- <svg>
					<circle cy={rScale(5)+1} cx={rScale(0)+1} r={rScale(0)} fill='none' stroke='black'></circle>
					<circle cy={rScale(5)+1} cx={rScale(5)+1} r={rScale(5)} fill='none' stroke='black'></circle>

					<text y={rScale(5)+rScale(0)} x={2*rScale(0)+1} r={rScale(0)}>{rScale(0)}%</text>
					<text y={rScale(5)+rScale(0)} x={2*rScale(5)+1} r={rScale(5)}>{rScale(5)}% of adult population</text>
				</svg> -->
			</div>
			
			<!-- <HowTo /> -->
		</div>
	</div>
</div>

<div id='beeswarm' class="chart beeswarm-chart">
	<LayerCake
		flatData={ data }
		data={ dataIn }
		{ rScale }
		rDomain={ rScale.domain() }
		rRange={ rScale.range() }
		{ zScale }
		zDomain={ zScale.domain() }
		zRange={ zScale.range() }
		padding={ { top: 0, right: 0, bottom: 0, left: 0 } }
	>
		<Svg>
			{#if render}

				{#if activeChart.type === 'diverging'}
					<ForceDiverging
						{ medium }
						{ diet_threshold }
						{ partisanship_scenario }
						collideStrength={ 0.1 }
						manyBodyStrength={ -0.5 }
						on:mouseenter={ handleMouseEnter }
						on:mouseleave={ handleMouseLeave }
						on:click={ handleClick }
					/>
				{/if}

				{#if activeChart.type === 'linear'}
					<ForceLinear
						{ medium }
						{ diet_threshold }
						{ partisanship_scenario }
						{ political_lean }
						collideStrength={ 0.1 }
						manyBodyStrength={ -0.5 }
						on:mouseenter={ handleMouseEnter }
						on:mouseleave={ handleMouseLeave }
						on:click={ handleClick }
					/>
				{/if}

			{/if}
		</Svg>
		<Html pointerEvents={!hidePopup}>
			<PopupOverlay 
				{ hidePopup }
				{ diet_threshold }
				{ partisanship_scenario }
				{ medium }
				period={ period || initPeriod }
				popup={ popup }
				on:closePopup={ handleClosePopup } 
			/>
		</Html>
	</LayerCake>
</div>

<style lang='scss'>
	.chart {
		width: 100%;
		height: 500px;
		position: relative;

		@media (min-width: $bp-3) {
			height: 800px;
		}
	}

	// .label {
	// 	color: var(--color);
	// 	font-weight: 700;
	// 	position: absolute;
	// 	text-shadow: 1px 1px 1px $white, -1px 1px 1px $white, 1px -1px 1px $white, -1px -1px 1px $white;
	// 	@include fs-sm;
	// }

	.chart-info-wrapper {
    display: grid;
    grid-template-columns: 1fr 2fr;
    margin-top: 10px;
		margin-bottom: 15px;
  }

	.legend {
		display: flex;
		align-items: flex-start;

		.legend-item {
			width: 50%;

			h5 {
				width: 100%;
			}
		}

		.legend-item-color {
			display: flex;
			align-items: center;
			flex-wrap: wrap;

			span {
				@include fs-xxs;
        font-weight: 300;
        letter-spacing: 1px;
        text-transform: uppercase;
			}

			.legend-block {
				background-color: var(--color);
				height: 25px;
				width: 25px;
			}
		}

		.legend-item-size {
			display: flex;
			flex-direction: column;
			height: 100%;

			div {
				flex-grow: 1;
				flex-shrink: 0;

				svg {
					height: 95px;
					width: 100%;
				}
			}
			// svg {
			// 	max-height: 100px;

			// 	text {
			// 		@include fs-xs;
			// 	}
			// }
		}

	}

	.controls {
    // grid-row: 1 / span 1;
    grid-column: 1 / span 1;
    display: grid;
    row-gap: 7px;
    grid-template-columns: auto auto 1fr;
    grid-template-rows: auto;
    grid-template-areas:
      "one two empty"
      "three four four";

    #period {
      grid-area: four;
    }
 
    .control-menu {
      display: flex;
      // align-items: center;
      flex-wrap: wrap;
      gap: 5px;
      
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
    }

		.control-menu {
			select {
				margin: 0;
				@include fs-sm;
			}
		}
  }
</style>

<!-- <Tooltip
	{evt}
	let:detail
>
	{@const tooltipData = { ...detail.props }}
	<div class='channel-label'>{tooltipData.channel_name}</div>
	<div
		class='cluster-label'
		style="--color: {colorMap.get(tooltipData.cluster)}"
	>{labelMap.get(tooltipData.cluster)}</div>
	{#each ['total_videos', 'subscribers'] as key}
		{@const keyCapitalized = key.replace(/^\w/, d => d.toUpperCase()).replace('_', ' ')}
		{@const value = tooltipData[key]}
		{#if value}
			<div class="row"><span>{keyCapitalized}:</span> {value.toLocaleString()}</div>
		{/if}
	{/each}
</Tooltip> -->