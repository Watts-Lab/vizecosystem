<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { csv } from "d3-fetch";
  import { autoType } from "d3-dsv";
	import { extent, group } from 'd3-array';


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
		data = res
    // parse data for 
		dataMap = group(
			res.filter(d => d.month === 4),
			d => d.state,
      // d => d.political_lean,
			d => d.medium, 
			d => d.diet_threshold,
			d => d.partisanship_scenario
		)
    fullDataMap = group(
			res.filter(d => d.month === 4),
			d => d.state, 
			d => d.diet_threshold,
			d => d.partisanship_scenario
		)
	})
</script>

<main>
	<div class='header-wrapper main-column'>
		<Title title={ title }></Title>
		<Description standfirst={ standfirst }></Description>
		<Authors authors={ authors }></Authors>
	</div>
	
	{#if data && data.length}
		<Beeswarm
			{ data }
			{ states }
			{ dataMap }
      { fullDataMap }
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

</style>