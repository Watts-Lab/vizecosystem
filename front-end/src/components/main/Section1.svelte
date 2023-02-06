<script lang="ts">
    // node_modules
    import { onMount } from "svelte";
    import { csv } from "d3-fetch";
    import { autoType } from "d3-dsv";
    import { group, extent } from "d3-array"
    import { scaleLinear } from 'd3-scale'
	// import { timeFormat } from 'd3-time-format'
    // import { format } from 'd3-format'

    // actions
    import inView from "../../actions/inView";

    // components
    // import StackedAreas from '../graphs/StackedAreas.svelte';
    import LineAreaChart from "../graphs/LineAreaChart.svelte";
    import DoubleRangeSlider from "../global/double-range-slider.svelte";

    // // import utils
	import { formatMonth } from '../../utils/format-dates';

    // locat data
    // import statesDict from '../../data/states.json'
    // const statesMap = new Map(statesDict.map(d => [d.state, d]))

    // props
    let loaded : boolean = false;
    export let once : boolean;
    export let copy : any[]
    export let refs : any[]
    export let captions : any[]

    // variable declaration
    const menuInfo : Map<string, string> = new Map([
        // ['political_lean', 'political_lean'],
        ['partisanship', 'partisanship'],
        ['diet', 'diet'],
        ['tv', 'tv']
    ]);
    let url : string = 'assets/data/dupe-data-by-gender.csv'
    let data : any[]
    let dataIn : Map<any,any>
    let xKey : string = 'date'
    let yKey : string = 'value'
    let zKey : number = 0
    let tvChecked : boolean = true;
    let scenarioChecked : boolean = true;
    let medium : string = tvChecked ? 'tv' : 'online'
    let partisanship_scenario : string = scenarioChecked ? 'lenient' : 'strict'
    const scaleRange : Function = scaleLinear();
    let start = 0
    let end = 1
    
    onMount(async () => {
        const res = await csv(url, autoType)
        data = res.map(d => ({ ...d, date: new Date(d.year, d.month, 1) }))

        const [ min, max ] = extent(data, d => +d.date);
        scaleRange.range([ min, max ])
	})

    const scaleDate : Function = (x) => {
        const date = new Date(scaleRange(x))
        date.setDate(1)
        date.setHours(0, 0, 0)
        date.setMilliseconds(0)

        return +date
    }

    $: if (data) {
        dataIn = group(
            data, 
            d => d.gender, 
            d => d.medium, 
            d => d.partisanship_scenario,
            d => d.age_group
        )
    }

    $: medium = tvChecked ? 'tv' : 'online'
    $: partisanship_scenario = scenarioChecked ? 'lenient' : 'strict'
    $: gender = 'All'
    $: age_group = 'under 18'
</script>

<div class="section section-1" use:inView={{ once }} on:enter={() => loaded = true }>
    <h1 class='section-title'>Section title</h1>
    <div class='copy copy-1'>
        {#each copy.slice(0,2) as d, i}
            <p>
                {d.value}
            </p>
        {/each}
    </div>
    <div class='chart-wrapper'>
        <div class='controls'>
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
        
            <div class='control control-switch'>
                <div class='control-title'>Partisanship</div>
                <div class='control-label {!scenarioChecked ? 'active' : ''}'>Lenient</div>
                <label class='switch'>
                <input type="checkbox" id="tv" name="tv" bind:checked={scenarioChecked}>
                <span class="slider"></span>
                </label>
                <div class='control-label {scenarioChecked ? 'active' : ''}'>Strict</div>
            </div>

            <div id='age-group' class='control control-menu'>
                <div class='control-title'>Age group</div>
                <select id="age-group-menu" name="age-group" bind:value={age_group}>
                    <option value='under 18'>Under 18</option>
                    <option value='25-34'>25-34</option>
                    <option value='35-44'>35-44</option>
                    <option value='45-54'>45-54</option>
                    <option value='55+'>55+</option>
                </select>
            </div>


            <div id='gender' class='control control-menu'>
                <div class='control-title'>Gender</div>
                <select id="gender-menu" name="location" bind:value={gender}>
                    <option value='All' selected>All</option>
                    <option value='Male'>Male</option>
                    <option value='Female'>Female</option>
                </select>
            </div>

            <!-- <div id='location' class='control control-menu'>
                <div class='control-title'>Location</div>
                <select id="location" name="location" bind:value={state}>
                    <option value='US' selected>United States</option>
                    {#each statesDict.sort((a,b) => a.state.localeCompare(b.state)) as states, i}
                        <option value={states.abbr}>{states.state}</option>
                    {/each}
                </select>
            </div> -->

            {#if loaded && data}
                <div id='period' class='control control-range'>
                    <div class='control-title'>Period</div>
                        <DoubleRangeSlider bind:start bind:end />
                        <div class="labels">
                            <div class="label">{ formatMonth(scaleRange(start)) }</div>
                            <div class="label">{ formatMonth(scaleRange(end)) }</div>
                        </div>
                </div>
            {/if}
        </div>
        {#if loaded && data}
            <LineAreaChart 
                data={ data }
                groupedData={
                    dataIn
                        .get(gender)
                        .get(medium)
                        .get(partisanship_scenario)
                        .get(age_group)
                }
                scaleRange={ scaleDate }
                { start }
                { end }
                { yKey } 
                { xKey } 
                { zKey }
                spanCol={12}
                customClass={'chart-medium'}
                formatTickX={formatMonth}
                url={ url }
                caption={captions[0].value}
            />
        {:else} <div class='chart-placeholder'></div>
        {/if}
    </div>
    <div class='copy copy-2'>
        {#each copy.slice(2) as d, i}
            <p>
                {d.value}
            </p>
        {/each}
    </div>
    <div class='references'>
        {#each refs as d}
            <p>
                {d.value}
            </p>
        {/each}
    </div>
</div>

<style lang='scss'>
    .section-1 {
        grid-template-columns: repeat(12, 1fr);
        column-gap: 0;
        grid-template-rows: auto auto auto 1fr auto auto;

        @media (min-width: $bp-3) {
            column-gap: 50px;
            grid-template-rows: auto auto auto auto 1fr auto;
        }
    }
    
    .chart-placeholder {
        height: 500px;
        background-color: lightgrey;
    }

    .section-title {
        border-bottom: 1pt solid black;
        // margin: 0 0 25px 0;
        grid-row: 1 / span 1;
        grid-column: span 12;
    }

    .copy-1 {
        grid-row: 2 / span 1;
        grid-column: span 12;

        @media (min-width: $bp-3) {
            grid-column: span 7;
        }
    }

    .copy-2 {
        grid-row: 5 / span 1;
        grid-column: span 12;

        @media (min-width: $bp-3) {
            grid-column: span 7;
        }
    }

    .references {
        grid-row: 6 / span 1;
        grid-column: span 12;

        @media (min-width: $bp-3) {
            grid-row: 5/ span 1;
            grid-column: span 5;
        }
    }

    .chart-wrapper {
        grid-row: 3 / span 1;
        grid-column: 1 / span 12;
    }

    .controls {
        display: flex;

        .control-switch, 
        .control-menu,
        .control-range {
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
        .control-range {
            flex-grow: 0.25;

            .labels {
                flex-grow: 1;
                display: flex;
                justify-content: space-between;

                .label {
                    @include fs-sm;
                }
            }
        }
    }

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