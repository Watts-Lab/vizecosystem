<script lang="ts">
	import { fade } from 'svelte/transition';

	import ChartPlaceholder from '$lib/components/global/chart-placeholder.svelte';
	import SelectMenu from '$lib/components/global/select-menu.svelte';
	import StackedAreas from '$lib/components/graphs/StackedAreas.svelte';
	import Caption from '$lib/components/graphs/layers/Caption.svelte';
	import Legend from '$lib/components/graphs/legend/legend.svelte';

  // utils
	import { formatYear } from '$lib/utils/format-dates';
	import { colorMapByMedium } from '$lib/utils/colors';

  export let data: any[]
  export let disableAgeGroup: boolean
  export let disableGender: boolean
  export let disableEthnicity: boolean
  export let userInteractedWithControls: boolean
	export let gender: string
  export let age_group: string
	export let ethnicity: string
	export let location: string
	export let disableMenus: boolean
  export let syncAxis: boolean
  export let userHasReachedLastLevel: boolean
  export let renderReachedLastLevelLabel: boolean
  export let stateMap: Map<string,string>
  export let ethnicityMap: Map<string,string>
  export let chartFilters: Map<string, Set<string>>
  export let dataMap: Map<string,any>
	export let rows : number[]
  export let d: any
	export let urlChart: string
  export let xDomain: Date[]
  export let toggleChartFilter: Function
  export let togglePreset: Function
  export let resetFilters: Function
	export let chartConfig: Map<string, { yDomain: number[], order: string[], colors: string[] }>
  export let xTicks: Date[]

  let preset: string
  let presetMap: Map<string, string> = new Map([
    ['all', 'All'], 
    ['news', 'News'], 
    ['entertainment', 'Entertainment'],
    ['social_media', 'Social Media']
  ])

  $: if (preset && preset !== 'all') {
    togglePreset(preset)
  } else if (preset === 'all') {
    resetFilters()
  }
</script>

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
      bind:userInteractedWithControls
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
      disabled={disableMenus || disableGender}
      bind:value={gender}
      bind:userInteractedWithControls
    />

    <SelectMenu 
      id='ethnicity' 
      title={'Ethnicity'}
      options={ethnicityMap}
      disabled={disableMenus || disableEthnicity}
      bind:value={ethnicity}
      bind:userInteractedWithControls
    />


    <SelectMenu 
      id='presets' 
      title={'Preset filters'}
      options={presetMap}
      disabled={false}
      bind:value={preset}
      bind:userInteractedWithControls
    />

    {#if userHasReachedLastLevel && renderReachedLastLevelLabel}
      <p 
        class='warning'
        in:fade
      >No further breakdown available</p>
    {/if}
  </div>

  {#if data} 
    <div class='chart-grid'>
      <div class='chart-inner'>
        <h4>TV</h4>
        <Legend 
          dataMap={
            dataMap
              .get('tv')
              .get(gender)
              .get(age_group)
              .get(ethnicity)
              .get(location)
              .get(xDomain[0])
          }
          colorMap={colorMapByMedium.get('tv').colorMap}
          toggleFilter={toggleChartFilter('tv')}
          enabledSet={chartFilters.get('tv')}
        />
        <StackedAreas 
          caption='tv'
          dataMap={
            dataMap
              .get('tv')
              .get(gender)
              .get(age_group)
              .get(ethnicity)
              .get(location)
          }
          {rows} 
          categories={chartConfig.get('tv').order} 
          colors={chartConfig.get('tv').colors}
          yDomain={chartConfig.get(syncAxis ? 'mobile': 'tv').yDomain}
          {xDomain}
          smallXDomain={chartConfig.get('tv').xDomain}
          {xTicks}
          formatter={formatYear}
          includeCaption={false}
          url={ urlChart }
          showAnnotation={
            false
          }
          chartFilters={chartFilters.get('tv')}
        />
      </div>

      <div class='chart-inner'>
        <h4>TV Streaming</h4>
        <Legend 
          dataMap={
            dataMap
              .get('streaming')
              .get(gender)
              .get(age_group)
              .get(ethnicity)
              .get(location)
              .get(xDomain[1])
          }
          colorMap={colorMapByMedium.get('streaming').colorMap}
          toggleFilter={toggleChartFilter('streaming')}
          enabledSet={chartFilters.get('streaming')}
        />
        <StackedAreas 
          caption='streaming'
          dataMap={
            dataMap
              .get('streaming')
              .get(gender)
              .get(age_group)
              .get(ethnicity)
              .get(location)
          }
          {rows} 
          categories={chartConfig.get('streaming').order} 
          colors={chartConfig.get('streaming').colors}
          yDomain={chartConfig.get(syncAxis ? 'mobile': 'streaming').yDomain}
          {xDomain}
          smallXDomain={chartConfig.get('streaming').xDomain}
          {xTicks}
          addTickYLabel={false}
          formatter={formatYear}
          includeCaption={false}
          url={ urlChart }
          chartFilters={chartFilters.get('streaming')}
        />
      </div>
    </div>
    {:else} <ChartPlaceholder height={300}/>
  {/if}
  <Caption caption={ d.value.captions } url={ urlChart } type={'single-cols'} />
</div>

<style lang="scss">
	.chart-container {
		grid-column: span 12;
        margin: 25px 0;

		h3 {
			margin-bottom: 1em;
		}

		.chart-grid {
			display: grid;
			column-gap: 15px;
			row-gap: 25px;
			grid-template-columns: repeat(2, 1fr);
			grid-template-rows: repeat(1, 1fr);
			margin: 15px 0 0 0;

			.chart-inner {
				display: flex;
				flex-direction: column;
				gap: 10px;
			}
		}
	}

	.controls {
        display: flex;
		position: relative;

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

		.warning {
			position: absolute;
			color: $css-lab-dark-red;
			top: -15px;
			left: 195px;
			@include fs-xs;
		}
	}
</style>
