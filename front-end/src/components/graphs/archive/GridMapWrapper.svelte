<script lang='ts'>
  // node_modules
	import { onMount } from 'svelte';
  import { csv } from "d3-fetch";
  import { autoType } from "d3-dsv";
  import { group } from "d3-array"

  // types
	import type State from '../../types/States';

  // components
  import SmallMultiplesRadar from './SmallMultiplesRadar.svelte';
  import HowTo from './HowTo.svelte';

  // utils
  import { formatMonth } from '../../utils/format-dates';
  import PopupOverlay from './tooltips/PopupOverlay.svelte';
  import SingleLineChart from './SingleLineChart.svelte';

  // props
  export let states : State[];
  export let xKey : string;
	export let yKey : string;
	export let zKey : number = 0;

  // variable declaration
  let url : string = 'assets/data/dupe-data-by-state.csv'
  let data : any[]
  let dataMap : Map<string,Object>
  let dietChecked : boolean = true;
  let scenarioChecked : boolean = true;
  let period : string = '3';
  let month : number = parseInt(period);
  let diet_threshold: number = dietChecked ? 75 : 50
  let partisanship_scenario : string = scenarioChecked ? 'lenient' : 'strict'

  onMount(async () => {
    const res = await csv(url, autoType)
    data = res //.map(d => ({ ...d, date: new Date(d.year, d.month, 1) })) 
    dataMap = group(data, d => d.state)
	})

  function handleOpenPopup(ev : any) { 
    overlayActive = true
    overlayData = ev.detail
  }

  function handleClosePopup() { 
    overlayActive = false
  }

  $: diet_threshold = dietChecked ? 75 : 50;
  $: partisanship_scenario = scenarioChecked ? 'lenient' : 'strict';
  $: month = parseInt(period);
  $: overlayActive = false;
  $: overlayData = []

  const menuInfo : Map<string,string> = new Map([
    ['partisanship', 'partisanship'],
    ['diet', 'diet'],
  ])
</script>

<div class="small-multiples grid-map">
  <div class='controls'>
    <div class='control control-switch'>
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
        <input type="checkbox" id="tv" name="tv" bind:checked={scenarioChecked}>
        <span class="slider"></span>
      </label>
      <div class='control-label {scenarioChecked ? 'active' : ''}'>Strict</div>
    </div>

    <div class='control control-switch'>
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

    <div class='control control-menu'>
      <div class='control-title'>Period</div>
      <select id="period" name="period" bind:value={period}>
        <option value=3 selected>March</option>
        <option value=4>April</option>
      </select>
    </div>
  </div>
  {#each states.slice(0,1) as state, i}
    <div id={state.abbr} class="state" style="--row: {state.row}; --col: {state.col}">
      <div class="label">{state.abbr}</div>
      <div class="state-chart-wrapper">
        {#if data}
          {@const d = dataMap.get(state.abbr)}
          <SmallMultiplesRadar
            data={d}
            flatData={data}
            { xKey }
            { yKey }
            { zKey }
            { diet_threshold }
            { partisanship_scenario }
            period={ month }
            formatTickX={ formatMonth }
            { state }
            on:openPopup={ handleOpenPopup }
          />
        {/if}
      </div>
    </div>
  {/each}
  <!-- {#if data}
    <HowTo 
      flatData={data}
    /> 
  {/if} -->
  <!-- <div class='overlay {overlayActive ? 'active' : ''}'></div> -->
  <PopupOverlay { overlayActive } { overlayData } on:closePopup={ handleClosePopup } />
</div>

<style lang='scss'>
  .grid-map {
    position: relative;
    grid-column: 1 / span last-line;
		grid-row: 3 / span last-line;
    display: grid;
    grid-template-columns: repeat(11, 1fr);
    grid-template-rows: repeat(8, 1fr);
    gap: 2px;
    padding: 0;

    @media (min-width: $column-width) {
			padding: 0 25px;
      }
  }

  .state {
    grid-row: var(--row);
    grid-column: var(--col);
    background-color: $off-white;
    // border-top: 1pt solid $off-white;
    // border-right: 1pt solid $off-white;
    padding: 2px;
    // display: grid;
    // grid-template-rows: auto 1fr;
    position: relative;

    .label {
      @include fs-xs;
      font-weight: 900;
      position: absolute;
      top: 0;
      left: 0;
    }

    .state-chart-wrapper {
      width: 100%;
      height: 100%;
    }
  }

  .controls {
    grid-row: 1 / span 1;
    height: 40px;
    grid-column: 1 / span 10;
    gap: 25px;
    display: flex;

    .control-switch, 
    .control-menu {
      display: flex;
      align-items: center;
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