<script lang='ts'>
  // node_modules
	import { createEventDispatcher, onMount } from 'svelte';
	import { csv } from "d3-fetch";
  import { autoType } from "d3-dsv";
  import { flatten } from 'layercake';
  import { fade } from 'svelte/transition';
  import { scaleLinear } from 'd3-scale';
  import { extent, group, max } from 'd3-array';

	const dispatch = createEventDispatcher();

  // components
  import LineAreaChart from '../LineAreaChart.svelte';
  import Table from '../Table.svelte';

  // // import utils
  import { formatMonth } from '../../../utils/format-dates';

  // prop declaration
  export let hidePopup : boolean;
  export let popup : any;
  export let diet_threshold : number;
	export let partisanship_scenario : string;
  export let medium : string;
  export let period : string;

  // variable declaration
  let xKey : string = 'date'
  let yKey : string = 'value'
  let zKey : number = 0
  let data : any[];
  let dataMap : Map<string|number, any>;
  let table : any[];
  let tableMap : Map<string|number, any>
  const urlChart : string  = 'assets/data/EchoCh-by_state_full-timeseries.csv'
  const urlTable : string  = 'assets/data/EchoCh-TV-by_state_audiences.csv'

  onMount(async () => {
    const resChart = await csv(urlChart, autoType)
		data = resChart.map(d => ({ ...d, date: new Date(d.year, d.month, 1) }))
    // parse data for 
		dataMap = group(
			data,
			d => d.state,
			d => d.medium,
		)

    // load data for tables
		// load data for map + line chart
		table = await csv(urlTable, autoType)
		tableMap = group(
			table,
			d => d.period,
			d => d.state,
			d => d.medium
		)
  })

  // event handlers
  function onClick() {
		dispatch('closePopup')
	}

</script>

<div class='overlay {!hidePopup ? 'active' : ''}'>
  {#if !hidePopup}
    {@const { abbr, state } = popup.detail.node}
    {@const dataChart = dataMap
      .get(abbr)
      .get(medium)
      .map(d => ({ ...d, value: Math.max(d.right_pct, d.left_pct)}))
    }
    {@const dataIn = flatten(dataChart.map(d => [
      { ...d, political_lean: 'R', value: d.right_pct },
      { ...d, political_lean: 'L', value: d.left_pct },
    ]))}
    {@const [ start, end ] = extent(dataChart, d => +d.date)}
    <h1 class='title' out:fade="{{ delay: 300 }}"><span>{abbr}</span> {state}</h1>
    <div class='overlay-col1-container'>
      <LineAreaChart 
        data={ dataChart }
        groupedData={ dataIn }
        scaleRange={scaleLinear().range([start, end])}
        start={ 0 }
        end={ 1 }
        { yKey } 
        { xKey } 
        { zKey }
        spanCol={12}
        customClass={ 'popup-overlay' }
        formatTickX={formatMonth}
        url={''}
        includeCaption={false}
      /> 
    </div>
    <p class='caption overlay-col1-caption'>
      <span>TV & Web news diet polarization</span> Lorem ipsum dolor sit amet consectetur 
      adipisicing elit. Odit, inventore impedit deleniti magnam eum eveniet 
      dolorum porro, saepe molestiae quis et, quia libero suscipit numquam?
    </p>
    
    {#if medium === 'tv'}
      {@const tableChart = tableMap
        .get(period)
        .get(abbr)
        .get(medium)
      }
      <div class='overlay-col2-container'>
        <Table 
          data={ tableChart }
        />
      </div>
    {/if}

    <p class='caption overlay-col2-caption'>
      <span>Most watched.</span> Lorem ipsum dolor sit amet consectetur 
      adipisicing elit. Odit, inventore impedit deleniti magnam eum eveniet 
      dolorum porro, saepe molestiae quis et, quia libero suscipit numquam?
    </p>
  {/if}
  <div class='close-button' on:click={() => onClick() }></div>
</div>

<style lang="scss">
  .placeholder {
    width: 100%;
    height: 100%;
    background-color: gainsboro;
  }
  .overlay {
    position: absolute;
    top: 0;
    left: -250%;
    width: 100%;
    height: 100%;
    background-color: $off-white;
    padding: 30px 50px;
    display: grid;
    column-gap: 50px;
    row-gap: 8px;
    grid-template-rows: auto 1fr 0.3fr;
    grid-template-columns: 1fr 1fr;
    transition: left 0.3s ease-out;
  }

  .overlay.active {
    left: 0;
  }

  .overlay-col1-container {
    grid-column: 1 / span 1;
    grid-row: 2 / span 1;
  }

  .overlay-col1-caption {
    grid-column: 1 / span 1;
    grid-row: 3 / span 1;
  }

  .overlay-col2-container {
    grid-column: 2 / span 1;
    grid-row: 2 / span 1;
  }
  .overlay-col2-caption {
    grid-column: 2 / span 1;
    grid-row: 3 / span 1;
  }


  .title {
    @include fs-xl;

    span {
      color: $mid-grey;
    }
  }

  .caption {
    @include fs-sm;

    span {
      font-weight: 700;
    }
  }

  .close-button {
    position: absolute;
    top: 25px;
    right: 25px;
  }

  .close-button:after {
    content: '\2715';
    @include fs-xl;
    line-height: 1;
  }
</style>