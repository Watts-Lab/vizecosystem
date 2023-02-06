<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { csv } from "d3-fetch";
  import { autoType } from "d3-dsv";
	import { group } from 'd3-array';
	import { scaleDiverging, scaleThreshold, scaleSqrt, scaleLinear } from 'd3-scale';

	// types
	import type Author from '../../types/Authors';
	import type ChartConfig from '../../types/ChartConfig';

	// components
	import Title from '../copy/Title.svelte';
	import Description from '../copy/Description.svelte';
	import Authors from '../copy/Authors.svelte';
	import Beeswarm from '../graphs/Beeswarm.svelte';
	import ChartPlaceholder from '../global/chart-placeholder.svelte';

	// prop declaration
	export let title : string;
	export let standfirst : any[] = [{value: 'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Commodi consequatur inventore exercitationem ex perferendis provident, earum cumque maiores quam quidem labore, mollitia odit eaque laborum?'}]
	export let authors : Author[];

	// local data
	import states from '../../data/states_centroids.json'

	// chart config
	
	let data : any[];
	let dataMap : Map<string, any>
  let fullDataMap : Map<string, any>
	const url : string  = 'assets/data/dupe-data-by-state-grid-map.csv'
	
	onMount(async () => {
		const res = await csv(url, autoType)
		data = res.map(d => ({ ...d, date: new Date(d.year, d.month, 1) }))
    // parse data for 
		dataMap = group(
			data,
			d => +d.date,
			d => d.state,
			d => d.medium, 
			d => d.diet_threshold,
			d => d.partisanship_scenario
		)

    fullDataMap = group(
			data,
			d => d.state,
			d => d.medium, 
			// d => d.diet_threshold,
			d => d.partisanship_scenario
			
		)
	})

	const chartConfig : Map<number,ChartConfig> = new Map([
		[0, {
			type: "diverging",
			rScale: scaleSqrt,
			rDomain: [0, 20],
			rRange: [3, 150],
			zScale: scaleThreshold,
			zDomain: [-0.75, -0.5, -0.1, 0.1, 0.5, 0.75],
			colorInterpolator: scaleDiverging,
			colorInterpolatorDomain: [-1, 0, 1],
			colorInterpolatorScheme: ["#011f5b", "gainsboro", "#990000"],
			colorPaletteAnchors: [-0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75]
		}],
		[1, {
			type: "linear",
			rScale: scaleSqrt,
			rDomain: [0, 20],
			rRange: [3, 150],
			zScale: scaleThreshold,
			zDomain: [0, 0.25, 0.5, 1],
			colorInterpolator: scaleLinear,
			colorInterpolatorDomain: [0, 1],
			colorInterpolatorScheme: "gainsboro",
			colorPaletteAnchors: [0, 0.25, 0.5, 0.75, 1]
		}],
	])

	$: chart = "0"
	$: activeChart = chartConfig.get(+chart)
	$: politicalChecked = true
</script>

<main>
	<div class='header-wrapper main-column'>
		<Title title={ title }></Title>
		<Description standfirst={ standfirst }></Description>
		<Authors authors={ authors }></Authors>
	</div>
	
	<div class='title-container main-column'>
			<h3 class='chart-title'>
				Partisan Segregation in the US:
				<select class='menu' bind:value={chart}>
					<option value="0">Comparison view</option>
					<option value="1">Single political lean view</option>
				</select>
			</h3>

			{#if activeChart.type === 'linear'}
				<div class='controls'>
					<div id='politicalLean' class='control control-switch'>
						<div class='control-title'>
							Political lean 
							<span 
								class='info' 
								on:mouseenter={() => {}} 
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
				</div>
			{/if}
	</div>


	
	{#if data && data.length}
		<Beeswarm
			{ data }
			{ states }
			{ dataMap }
      { fullDataMap }
			{ activeChart }
			{ politicalChecked }
		/>
		{:else} <ChartPlaceholder />
	{/if}
</main>

<style lang='scss'>
	main {
		max-width: $column-width * 1.25;
		margin: 0 auto;
	}

	.header-wrapper {
		@include grid-mobile;
		@include centerH;
		align-items: center;
		margin-top: 25px;

		@media (min-width: $bp-3) {
			@include grid;
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
		max-height: 45px;
		display: grid;
    row-gap: 5px;
    grid-template-columns: auto auto 1fr;
    grid-template-rows: auto;
    grid-template-areas:
      "one two empty"
      "three four four";

		#politicalLean {
      grid-area: one;
    }

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
				font-weight: 700;
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
    // background-color: #ccc;
		background-color: rgb(56, 78, 123);
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
    // background-color: #2196F3;
		background-color: rgb(170, 55, 55);
  }

  input:focus + .slider {
    box-shadow: 0 0 1px rgb(170, 55, 55);
  }

  input:checked + .slider:before {
    -webkit-transform: translateX(11px);
    -ms-transform: translateX(11px);
    transform: translateX(11px);
  }

</style>