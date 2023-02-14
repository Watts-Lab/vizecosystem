<script lang='ts'>
  // node_modules
	import { createEventDispatcher } from 'svelte';
  import { flatten } from 'layercake';
  import { fade } from 'svelte/transition';
  import { scaleLinear } from 'd3-scale';
  import { extent } from 'd3-array';

	const dispatch = createEventDispatcher();

  // components
  import LineAreaChart from '../LineAreaChart.svelte';
  import Table from '../Table.svelte';

  // // import utils
  import { formatMonth } from '../../../utils/format-dates';

  // prop declaration
  export let hidePopup : boolean;
  export let popup : any;
  export let dataMap : Map<string|number, any>;
  export let tableMap : Map<string|number, any>;
  export let diet_threshold : number;
	export let partisanship_scenario : string;
  export let medium : string;

  // variable declaration
  let xKey : string = 'date'
  let yKey : string = 'value'
  let zKey : number = 0

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
      .get(partisanship_scenario)
    }
    <!-- .get(diet_threshold) -->
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

    {@const tableChart = tableMap
      .get(abbr)
      .get(medium)
      .get(diet_threshold)
      .get(partisanship_scenario)
    }
    <div class='overlay-col2-container'>
      <Table 
        data={ tableChart }
      />
    </div>

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