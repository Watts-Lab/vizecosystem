<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
  import { csv } from "d3-fetch";
  import { autoType } from "d3-dsv";
  import { group, rollup, extent } from 'd3-array';

	// import state data
  import states from '$lib/data/states.json'
  import copy from '$lib/data/copy.json'
  const body: any[] = copy['overall-news-consumption']

  // components
  import Grid from "$lib/components/layouts/overall-news-consumption-grid.svelte";

	// actions
	import inView from "$lib/actions/inView";

	// import utils
	import { colorMapByMedium } from '$lib/utils/colors';
	import parseCopy from '$lib/utils/parse-copy';
	
	// prop declaration
	let loaded : boolean = false;

	// chart config
	let data : any[]
	let dataMap : Map<string, any>
	let rows : number[]
	let xTicks : Date[]
	let xDomain : Date[]
	let axisChecked : boolean = true
	let chartConfig : Map<string, { yDomain: number[], order: string[], colors: string[] }>
	let extentMapper: Map<string, Date[]>
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

    extentMapper = rollup(data, (v: any) => Array.from(new Set(v.map((y: any) => y.year))), (d: any) => d.medium)

		rows = Array.from(new Set(data.map((d: any) => +d.date)))
		xTicks = Array.from(new Set(data.map(d => d.year))).map(d => new Date(d, 0, 1))
		xDomain = extent(data, (d: any) => d.date)
	})

	$: if (data) chartConfig = new Map([
		['tv', {
			order: Array.from(colorMapByMedium.get('tv')!.colorMap).map(d => d[0]),
			colors: Array.from(colorMapByMedium.get('tv')!.colorMap).map(d => d[1].color),
			yDomain: [0, 300],
      xDomain,
      xTicks,
		}
		],
		['web', {
			order: Array.from(colorMapByMedium.get('web')!.colorMap).map(d => d[0]),
			colors: Array.from(colorMapByMedium.get('web')!.colorMap).map(d => d[1].color),
			yDomain: [0, 100],
      xDomain,
      xTicks,
		}],
		['mobile', {
			order: Array.from(colorMapByMedium.get('mobile')!.colorMap).map(d => d[0]),
			colors: Array.from(colorMapByMedium.get('mobile')!.colorMap).map(d => d[1].color),
			yDomain: [0, 300],
      xDomain: extent(data.filter((e: any) => e.medium === 'mobile'), (d: any) => d.date),
      xTicks: extentMapper.get('mobile'),
		}],
		['tablet', {
			order: Array.from(colorMapByMedium.get('tablet')!.colorMap).map(d => d[0]),
			colors: Array.from(colorMapByMedium.get('tablet')!.colorMap).map(d => d[1].color),
			yDomain: [0, 300],
      xDomain: extent(data.filter((e: any) => e.medium === 'tablet'), (d: any) => d.date),
      xTicks: extentMapper.get('tablet'),
		}],
		['streaming', {
			order: Array.from(colorMapByMedium.get('streaming')!.colorMap).map(d => d[0]),
			colors: Array.from(colorMapByMedium.get('streaming')!.colorMap).map(d => d[1].color),
			yDomain: [0, 100],
      xDomain: extent(data.filter((e: any) => e.medium === 'streaming'), (d: any) => d.date),
      xTicks: extentMapper.get('streaming'),
		}],
	])

  let chartFilters: Map<string, Set<string>>
  $: chartFilters = new Map([
    ['tv', new Set(Array.from(colorMapByMedium.get('tv')!.colorMap).map(d => d[0]))],
    ['web', new Set(Array.from(colorMapByMedium.get('web')!.colorMap).map(d => d[0]))],
    ['mobile', new Set(Array.from(colorMapByMedium.get('mobile')!.colorMap).map(d => d[0]))],
    ['tablet', new Set(Array.from(colorMapByMedium.get('tablet')!.colorMap).map(d => d[0]))],
    ['streaming', new Set(Array.from(colorMapByMedium.get('streaming')!.colorMap).map(d => d[0]))],
  ])

  function toggleChartFilter(medium: string) {
    return (category: string) => {
      const newChartFilter = new Map(chartFilters)
      const set = new Set(newChartFilter.get(medium))

      if (set.has(category)) {
        set.delete(category)
      }
      else {
        set.add(category)
      }

      newChartFilter.set(medium, set)
      chartFilters = newChartFilter
    }
  }
  
  function togglePreset(category: string) {
    const newChartFilter = new Map(chartFilters)
    const set = new Set([category])

    for (const [key, _] of newChartFilter) {
      newChartFilter.set(key, set);
    }

    chartFilters = newChartFilter
  }

  function resetFilters() {
    chartFilters = new Map([
      ['tv', new Set(Array.from(colorMapByMedium.get('tv')!.colorMap).map(d => d[0]))],
      ['web', new Set(Array.from(colorMapByMedium.get('web')!.colorMap).map(d => d[0]))],
      ['mobile', new Set(Array.from(colorMapByMedium.get('mobile')!.colorMap).map(d => d[0]))],
      ['tablet', new Set(Array.from(colorMapByMedium.get('tablet')!.colorMap).map(d => d[0]))],
      ['streaming', new Set(Array.from(colorMapByMedium.get('streaming')!.colorMap).map(d => d[0]))],
    ])
  }   

	$: syncAxis = axisChecked === true
	$: gender = 'All'
  $: age_group = 'All'
	$: ethnicity = 'All'
	$: location = 'US'
	$: disableMenus = location !== 'US'
	$: userInteractedWithControls = false;

	function resetAge() { age_group = 'All' }
  function resetGender() { gender = 'All' }
	function resetEthnicity() { ethnicity = 'All' }
	function resetState() { location = 'US' }

	$: if (location !== 'US') { resetGender(); resetAge(); resetEthnicity(); }
	$: if (age_group !== 'All' || gender !== 'All' || ethnicity !== 'All') { resetState() }
	$: disableAgeGroup = ethnicity !== 'All' && gender !== 'All'
	$: disableGender = age_group !== 'All' && ethnicity !== 'All'
	$: disableEthnicity = age_group !== 'All' && gender !== 'All'
	$: if ((disableAgeGroup || disableGender || disableEthnicity) || disableMenus) {
		userHasReachedLastLevel = true;
		renderReachedLastLevelLabel = true;
		setTimeout(() => renderReachedLastLevelLabel = false, 5000);
	}
	
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

	$: userHasReachedLastLevel = false
	$: renderReachedLastLevelLabel = false;
</script>

<div class="section" use:inView={{ once: true }} on:enter={() => loaded = true }>
	{#each body as d}
		{#if d.type === 'text'}
			<p class='copy'>
				{@html parseCopy(d.value)}
			</p>
    {:else if d.type === 'title'} <h1 class='section-title'>{ d.value }</h1>
		{:else} 
      <Grid 
        {data}
        {disableAgeGroup}
        {disableGender}
        {disableEthnicity}
        {userInteractedWithControls}
        {gender}
        {age_group}
        {ethnicity}
        {location}
        {disableMenus}
        {syncAxis}
        {userHasReachedLastLevel}
        {stateMap}
        {ethnicityMap}
        {rows}
        {d}
        {dataMap}
        {chartFilters}
        {urlChart}
        {renderReachedLastLevelLabel}
        {xDomain}
        {xTicks}
        {toggleChartFilter}
        {togglePreset}
        {resetFilters}
        {chartConfig}
      />
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

</style>
