<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { LayerCake, Svg, Html } from 'layercake';
	import { piecewise, interpolateRgb } from 'd3-interpolate';

	// types
	import type ChartConfig from '../../types/ChartConfig';

	// components
	import ForceDiverging from './ForceDiverging.svelte';
	import ForceLinear from './ForceLinear.svelte';
	import PopupOverlay from './tooltips/PopupOverlay.svelte';
	import ControlSwitch from '../global/control-switch.svelte';
	import Caption from './atoms/Caption.svelte';
	
	// local data
	import statesDict from '../../data/states.json'
	import copy_data from '../../data/copy.json'

	const statesMap = new Map(statesDict.map(d => [d.state, d]))

	// props declaration
	export let data : any[];
	export let states : any[];
	export let dataMap : Map<string|number, any>
	export let fullDataMap : Map<string|number, any>
	export let activeChart : ChartConfig;
	export let caption : string = '';
	export let url : string = '';
	export let includeCaption : boolean = true;

	// variable declaration
	let colorInterpolator : any;
	export let politicalChecked : boolean;
	let dietChecked : boolean = false
  	let scenarioChecked : boolean = true
	let tvChecked : boolean = false
	$: political_lean = politicalChecked ? 'R' : 'L'
	$: medium = tvChecked ? 'web' : 'tv'
	$: diet_threshold = dietChecked ? 75 : 50
  	$: partisanship_scenario = scenarioChecked ? 'lenient' : 'stringent'

	// tooltip togglers
	$: tooltip = null;
	let hideTooltip : boolean = true;
	// overlay pop up togglers
	$: popup = null;
	let hidePopup : boolean = true;
	// other global vars
	let render : boolean = false;
	let renderAnnotation : boolean = false;
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

	const dates = [
		'Since 2016',
		'Last 3 months', 
		'Last 6 months', 
		'Last 12 months',
	]
	let initPeriod = 'Since 2016'
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
	$: colorAnchors = activeChart.zDomain
	
	$: zScale = activeChart.zScale()
		.domain(activeChart.zDomain)
		.range(colorPalette)

	onMount(() => {
		setTimeout(() => renderAnnotation = true, 2000)
	})
	
</script>

<div class='chart-info-wrapper main-column'>
	<div class='controls'>
		<ControlSwitch 
			id='medium' 
			title={copy_data.controls.medium.title}
			labels={[ 'TV', 'Web' ]}
			info={copy_data.controls.medium.description}
			bind:checked={ tvChecked } 
		/>

		<!-- inverting labels manually for now -->
		<ControlSwitch 
			id='partisanship' 
			title={copy_data.controls.medium.title}
			labels={[ 'Stringent', 'Lenient' ]} 
			info={copy_data.controls.partisanship.description}
			bind:checked={ scenarioChecked } 
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
				<span class='legend-block-label legend-block-label-L'>More left</span>
			{/if}
			{#each colorPalette as d, i}
				{@const anchor = colorAnchors[i]}
				<div class='legend-block' style="--color: {d}">
					{#if anchor !== undefined}
						<div
							class={`legend-anchor-label legend-anchor-label-${anchor > 0 ? 'R' : 'L'}`}
						>
							{Math.abs(anchor).toLocaleString('en-NZ', { style: 'percent', maximumFractionDigits: 1, minimumFractionDigits: 0 })}
						</div>
					{/if}
				</div>
			{/each}
			<span class='legend-block-label legend-block-label-R'>More { political_lean === 'L' ? 'left' : 'right' }</span>
		</div>
		
		<div class='legend-item legend-item-size'>
			<h5>Echo chamber size</h5>
			<div>
				<svg>
					<circle 
						cy={0} 
						cx={rScale(activeChart.rDomain[1] / 2) + 1}
						r={rScale(activeChart.rDomain[0])} 
						fill='none' 
						stroke='black'
						class='legend-circle'
					></circle>
					<text
						y={rScale(activeChart.rDomain[0]) + 2} 
						x={rScale(activeChart.rDomain[1] / 2)}
						class='legend-circle-label'
					>
						{activeChart.rDomain[0].toLocaleString('en-NZ', { notation: "compact" })}
					</text>

					<circle 
						cy={0} 
						cx={rScale(activeChart.rDomain[1] / 2) + 1}
						r={rScale(activeChart.rDomain[1] / 18)} 
						fill='none' 
						stroke='black'
						class='legend-circle'
					></circle>
					<text
						y={rScale(activeChart.rDomain[1] / 18) + 2} 
						x={rScale(activeChart.rDomain[1] / 2)}
						class='legend-circle-label'
					>
						{(activeChart.rDomain[1] / 18).toLocaleString('en-NZ', { notation: "compact" })}
					</text>
					
					<circle 
						cy={0} 
						cx={rScale(activeChart.rDomain[1] / 2)} 
						r={rScale(activeChart.rDomain[1] / 4.5)} 
						fill='none' 
						stroke='black'
						class='legend-circle'
					></circle> 
					<text 
						y={rScale(activeChart.rDomain[1] / 4.5) + 2} 
						x={rScale(activeChart.rDomain[1] / 2)}
						class='legend-circle-label'
					>
						{(activeChart.rDomain[1] / 4.5).toLocaleString('en-NZ', { notation: "compact" })}
					</text>

					<circle 
						cy={0} 
						cx={rScale(activeChart.rDomain[1] / 2)} 
						r={rScale(activeChart.rDomain[1] / 2)} 
						fill='none' 
						stroke='black'
						class='legend-circle'
					></circle> 
					<text 
						y={rScale(activeChart.rDomain[1] / 2) + 2} 
						x={rScale(activeChart.rDomain[1] / 2)}
						class='legend-circle-label'
					>
						{(activeChart.rDomain[1] / 2).toLocaleString('en-NZ', { notation: "compact" })}
					</text>
				</svg>
			</div>
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
						{ renderAnnotation }
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
{#if includeCaption}
	<Caption { caption } { url } type={'single-cols'} />
{/if}


<style lang='scss'>
	.chart {
		width: 100%;
		height: 730px;
		position: relative;
		grid-row: 5 / span 1;
		grid-column: span 12;

		@media (min-width: $bp-3) {
			height: 800px;
		}
	}

	.chart-info-wrapper {
		display: grid;
		grid-template-columns: 1fr 2fr;
		margin-top: 10px;
		margin-bottom: 15px;
		grid-row: 4 / span 1;
		grid-column: span 12;
	}

	.legend {
		display: flex;
		align-items: flex-start;

		.legend-item {
			row-gap: 5px;
			h5 {
				width: 100%;
			}
		}

		.legend-item-color {
			width: 65%;
			display: flex;
			align-items: center;
			flex-wrap: wrap;

			.legend-block-label {
				@include fs-xxs;
				font-weight: 300;
				letter-spacing: 1px;
				text-transform: uppercase;
			}

			.legend-block-label-L {
				margin-right: 5px;
			}

			.legend-block-label-R {
				margin-left: 5px;
			}

			.legend-block {
				width: 35%;
				background-color: var(--color);
				height: 25px;
				width: 25px;
				border-left: 1pt solid $white;

				.legend-anchor-label {
					@include fs-xxxs;
					position: relative;
					width: 100%;
					top: 24px;
					left: 14px;
					text-align: center;
				}
			}

			.legend-block:first-of-type {
				border-left: none;
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
				
					text {
						@include fs-xs;
						paint-order: stroke;
						stroke-width: 5px;
						stroke-linecap: butt;
						stroke-linejoin: miter;
						stroke: $white;
					}
				}
			}
		}

	}

	.controls {
		grid-column: 1 / span 1;
		display: grid;
		row-gap: 7px;
		grid-template-columns: auto auto 1fr;
		grid-template-rows: auto;
		grid-template-areas:
		"one two empty"
		"four four four";

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
