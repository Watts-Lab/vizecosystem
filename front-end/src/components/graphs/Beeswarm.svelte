<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { LayerCake, Svg, Html } from 'layercake';
	import { scaleDiverging, scaleThreshold, scaleSqrt } from 'd3-scale';
	import { piecewise, interpolateRgb } from 'd3-interpolate'
	// import { extent, group } from 'd3-array';

	// types

	// components
	import Force from './Force.svelte';
	import PopupOverlay from './tooltips/PopupOverlay.svelte';

	// // utils
	
	// local data
	import statesDict from '../../data/states.json'
	const statesMap = new Map(statesDict.map(d => [d.state, d]))

	// props declaration
	export let data : any[];
	export let states : any[];
	export let dataMap : Map<string, any>
	export let fullDataMap : Map<string, any>

	// variable declaration
	const menuInfo : Map<string, string> = new Map([
    // ['political_lean', 'political_lean'],
    ['partisanship', 'partisanship'],
    ['diet', 'diet'],
		['tv', 'tv']
  ]);
  // let politicalChecked : boolean = true;
	// let political_lean: string = politicalChecked ? 'L' : 'R'
	let dietChecked : boolean = true;
	// let diet_threshold: number = dietChecked ? 75 : 50
  let scenarioChecked : boolean = true;
  // let partisanship_scenario : string = scenarioChecked ? 'lenient' : 'strict'
	let tvChecked : boolean = true
	// let medium : string = scenarioChecked ? 'tv' : 'online'
	let period : string = '3';
	// $: political_lean = politicalChecked ? 'L' : 'R'
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

	const breakpoints = [-0.5, -0.25, 0.25, 0.5]

	const colorInterpolator = scaleDiverging()
		.domain([-2, 0, 2])
		.interpolator(piecewise(
			interpolateRgb.gamma(0.5), 
			["#011f5b", "#D4BAC7", "#990000"]
		))

	const colorPalette : number[] = [-1, -0.5, 0, 0.5, 1].map(colorInterpolator);

	const rScale = scaleSqrt()
		.domain([0, 20])
		.range([10, 50]);
	const zScale = scaleThreshold()
		.domain(breakpoints)
		.range(colorPalette)

</script>

<div class='chart-info-wrapper main-column'>
	<div class='controls'>
		<!-- <div class='control control-switch'>
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
		</div> -->
		
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
			<h5>Partisan lean difference</h5>
			<span>More left</span>
			{#each colorPalette as d}
				<div class='legend-block' style="--color: {d}"></div>
			{/each}
			<span>More right</span>
		</div>
		
		<div class='legend-item legend-item-size'>
			<h5>Per capita news consumption</h5>
			<svg>
				<text x={rScale(20) + rScale(10) + 2} y={rScale(10)}>20 per 100,000</text>
				<circle cx={rScale(20) + 2} cy={rScale(20) + 2} r={rScale(10)} fill='none' stroke='black' stroke-width={1}></circle>
				<circle cx={rScale(20) + 2} cy={rScale(20) + rScale(10/2)} r={rScale(0)} fill='none' stroke='black' stroke-width={1}></circle>
				<text x={rScale(20) + rScale(0) + 2} y={rScale(20) + rScale(10/2) - 8}>5</text>
			</svg>
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
			<Force
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
			svg {
				max-height: 100px;

				text {
					@include fs-xs;
				}
			}
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