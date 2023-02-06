<script lang='ts'>
  // node_modules
	import { createEventDispatcher } from 'svelte';
  import { flatten } from 'layercake';
  import { fade } from 'svelte/transition';
  import { scaleLinear } from 'd3-scale';
  import { extent } from 'd3-array';

	const dispatch = createEventDispatcher();

  // componenents
  import RadarChart from "../RadarChart.svelte";
  import LineAreaChart from '../LineAreaChart.svelte';

  // // import utils
  import { formatMonth } from '../../../utils/format-dates';

  // prop declaration
  export let hidePopup : boolean;
  export let popup : any;
  export let dataMap : Map<string|number, any>;
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
    {@const data = dataMap
      .get(abbr)
      .get(medium)
      .get(partisanship_scenario)
    }
    <!-- .get(diet_threshold) -->
    {@const dataIn = flatten(data.map(d => [
      { ...d, political_lean: 'R', value: d.right_pct },
      { ...d, political_lean: 'L', value: d.left_pct },
    ]))}
    {@const [ start, end ] = extent(data, d => +d.date)}
    <h1 class='title' out:fade="{{ delay: 300 }}"><span>{abbr}</span> {state}</h1>
    <div class='overlay-bowtie-container'>
      <!-- <RadarChart
        data={ dataMap.get(abbr).get(diet_threshold).get(partisanship_scenario) }
        customClass={ 'popupOverlay' }
      /> -->
      <LineAreaChart 
        data={ data }
        groupedData={ dataIn }
        scaleRange={scaleLinear().range([start, end])}
        start={ 0 }
        end={ 1 }
        { yKey } 
        { xKey } 
        { zKey }
        spanCol={12}
        customClass={ 'popupOverlay' }
        formatTickX={formatMonth}
        url={''}
        includeCaption={false}
      />
    </div>
    <!-- <p class='caption overlay-bowtie-caption'>
      <span>TV & Web news diet polarization</span> Lorem ipsum dolor sit amet consectetur 
      adipisicing elit. Odit, inventore impedit deleniti magnam eum eveniet 
      dolorum porro, saepe molestiae quis et, quia libero suscipit numquam?
    </p> -->


    <!-- <div class='overlay-other-container'>
      <div class='placeholder'></div>
    </div>

    <p class='caption overlay-other-caption'>
      <span>Lorem, ipsum dolor.</span> Lorem ipsum dolor, sit amet consectetur 
      adipisicing elit. Culpa doloribus autem provident, ea voluptatem aliquid 
      temporibus, obcaecati totam aliquam ipsum ab cupiditate necessitatibus 
      incidunt repellendus, itaque maiores rerum rem quidem sequi. Debitis, 
      maxime! Est, beatae asperiores quasi minima quis sunt repellat. Quaerat 
      nam consequuntur dicta est eos minima doloremque, esse sint sed praesentium 
      expedita reiciendis blanditiis recusandae? Recusandae ipsum maxime libero 
      voluptatibus. Labore, architecto possimus cum eaque quidem placeat ab. 
      Temporibus error accusantium at? Deleniti illo a, quia odit doloremque 
      voluptas animi ea quasi suscipit iste distinctio, consectetur consequatur 
      maiores tempore deserunt excepturi voluptatem repellendus vitae? Sequi ea 
      illum sunt.
    </p> -->
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
    padding: 50px;
    display: grid;
    column-gap: 50px;
    grid-template-rows: auto 1fr 0.3fr;
    grid-template-columns: 1fr 1fr;
    transition: left 0.3s ease-out;
  }

  .overlay.active {
    left: 0;
  }

  .overlay-bowtie-container {
    grid-column: 1 / span 1;
    grid-row: 2 / span 1;
  }

  .overlay-bowtie-caption {
    grid-column: 1 / span 1;
    grid-row: 3 / span 1;
  }

  .overlay-other-container {
    grid-column: 2 / span 1;
    grid-row: 2 / span 1;
  }
  .overlay-other-caption {
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