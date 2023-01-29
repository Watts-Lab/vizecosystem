<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { LayerCake, Svg, Html } from 'layercake';
	import { scaleDiverging, scaleThreshold, scaleSqrt } from 'd3-scale';
	import { piecewise, interpolateRgb } from 'd3-interpolate'
	// import { extent, group } from 'd3-array';

	// types
	import type ChartConfig from '../../types/ChartConfig';

	// components
	import Force from './Force_2.svelte';
	import ForceDiverging from './Force_2.svelte';
	import ForceLinear from './Force_3.svelte';
	import PopupOverlay from './tooltips/PopupOverlay.svelte';
	// import HowTo from './archive/HowTo.svelte'

	// // utils
	
	// local data
	import statesDict from '../../data/states.json'

	const statesMap = new Map(statesDict.map(d => [d.state, d]))

	// props declaration
	export let data : any[];
	export let states : any[];
	export let dataMap : Map<string, any>
	export let fullDataMap : Map<string, any>
	export let activeChart : ChartConfig;

	// variable declaration
	const menuInfo : Map<string, string> = new Map([
    // ['political_lean', 'political_lean'],
    ['partisanship', 'partisanship'],
    ['diet', 'diet'],
		['tv', 'tv']
  ]);
	let colorInterpolator;
	let politicalChecked : boolean = true;
	let dietChecked : boolean = true;
  let scenarioChecked : boolean = true;
	let tvChecked : boolean = true
	let period : string = '3';
	$: political_lean = politicalChecked ? 'R' : 'L'
	$: medium = tvChecked ? 'tv' : 'online';
	$: diet_threshold = dietChecked ? 75 : 50;
  $: partisanship_scenario = scenarioChecked ? 'lenient' : 'strict';

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

	// reactive variables
	$: dataIn = states
		.map(d => {
			const { abbr } = statesMap.get(d.state)
			const data = dataMap
				.get(abbr)
				// .get(political_lean)
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
		{#if activeChart.type === 'linear'}
			<div class='control control-switch'>
				<div class='control-title'>
					Political lean 
					<span 
						class='info' 
						on:mouseenter={() => { console.log(menuInfo.get('tv')) }} 
						on:mouseleave={() => {}}
					>?</span>
				</div>
				<div class='control-label {!politicalChecked ? 'active' : ''}'>L</div>
				<label class='switch'>
					<input type="checkbox" id="medium" name="medium" bind:checked={politicalChecked}>
					<span class="slider"></span>
				</label>
				<div class='control-label {politicalChecked ? 'active' : ''}'>R</div>
			</div>
		{/if}
		
		<div id='medium' class='control control-switch'>
			<div class='control-title'>
				Medium 
				<span 
					class='info' 
					on:mouseenter={() => { console.log(menuInfo.get('tv')) }} 
					on:mouseleave={() => {}}
				>?</span>
			</div>
			<div class='control-label {!tvChecked ? 'active' : ''}'>TV</div>
			<label class='switch'>
				<input type="checkbox" id="medium" name="medium" bind:checked={tvChecked}>
				<span class="slider"></span>
			</label>
			<div class='control-label {tvChecked ? 'active' : ''}'>Web</div>
		</div>

		<div id='partisanship' class='control control-switch'>
			<div class='control-title'>
				Partisanship 
				<span 
					class='info' 
					on:mouseenter={() => { console.log(menuInfo.get('partisanship')) }} 
					on:mouseleave={() => {}}
				>?</span>
			</div>
			<div class='control-label {!scenarioChecked ? 'active' : ''}'>Lenient</div>
			<label class='switch'>
				<input type="checkbox" id="partisanship" name="partisanship" bind:checked={scenarioChecked}>
				<span class="slider"></span>
			</label>
			<div class='control-label {scenarioChecked ? 'active' : ''}'>Strict</div>
		</div>

		<div id='diet' class='control control-switch'>
			<div class='control-title'>
				Diet % 
				<span 
					class='info' 
					on:mouseenter={() => { console.log(menuInfo.get('diet')) }} 
					on:mouseleave={() => {}}
				>?</span>
			</div>
			<div class='control-label {!dietChecked ? 'active' : ''}'>50%</div>
			<label class='switch'>
				<input type="checkbox" id="diet" name="diet" bind:checked={dietChecked}>
				<span class="slider"></span>
			</label>
			<div class='control-label {dietChecked ? 'active' : ''}'>75%</div>
		</div>

		<div id='period' class='control control-menu'>
			<div class='control-title'>Period</div>
			<select id="period" name="period" bind:value={period}>
				<option value=3 selected>March</option>
				<option value=4>April</option>
			</select>
		</div>
	</div>
	<div class='legend'>
		<div class='legend-item legend-item-color'>
			<h5>Partisan lean</h5>
			<span>More left</span>
			{#each colorPalette as d}
				<div class='legend-block' style="--color: {d}"></div>
			{/each}
			<span>More right</span>
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
					collideStrength={ 0.1 }
					manyBodyStrength={ -0.5 }
					on:mouseenter={ handleMouseEnter }
					on:mouseleave={ handleMouseLeave }
					on:click={ handleClick }
				/>
			{/if}

		{/if}
		<!-- { political_lean } -->
	</Svg>
	<Html pointerEvents={!hidePopup}>
		{#if hideTooltip !== true}
			{@const { abbr, x, y, r } = tooltip.detail.node }
			{@const xAng = (x - 16) + r * Math.cos(-3 * Math.PI / 4)}
			{@const yAng = (y - 16) + r * Math.sin(-3 * Math.PI / 4)}
			<div
				class='label'
				style='transform: translate({xAng}px, {yAng}px)'
			>
				{ abbr }
			</div>
		{/if}

		<PopupOverlay 
			{ hidePopup }
			{ diet_threshold }
			{ partisanship_scenario }
			popup={ popup }
			dataMap={ fullDataMap }
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
			height: 600px
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
    margin-top: 50px;
		// margin-bottom: 50px;
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
    row-gap: 5px;
    grid-template-columns: auto auto 1fr;
    grid-template-rows: auto;
    grid-template-areas:
      "one two empty"
      "three four four";

    #medium {
      grid-area: one;
    }

    #partisanship {
      grid-area: two;
    }

    #diet {
      grid-area: three;
    }

    #period {
      grid-area: four;
    }

    // .control {
    //   width: 50%;
    // }

    .control-switch, 
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
  }

  /* The switch */
  $switch-width: 35px;
  $switch-height: 24px;

  .switch {
    position: relative;
    display: inline-block;
    width: $switch-width;
    height: $switch-height;

    input {
      opacity: 0;
      width: 0;
      height: 0;
    }
  }

  /* The slider */
  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: .4s;
    transition: .4s;
  }

  .slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    -webkit-transition: .4s;
    transition: .4s;
  }

  input:checked + .slider {
    background-color: #2196F3;
  }

  input:focus + .slider {
    box-shadow: 0 0 1px #2196F3;
  }

  input:checked + .slider:before {
    -webkit-transform: translateX(11px);
    -ms-transform: translateX(11px);
    transform: translateX(11px);
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