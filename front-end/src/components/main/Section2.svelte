<script lang="ts">
    // node_modules
    import { onMount } from "svelte";
    import { csv } from "d3-fetch";
    import { autoType } from "d3-dsv";
    import { group, extent } from "d3-array"
    import { scaleLinear } from 'd3-scale'
	
    // actions
    import inView from "../../actions/inView";

    // components
    import LineAreaChart from "../graphs/LineAreaChart.svelte";
    import DoubleRangeSlider from "../global/double-range-slider.svelte";
    import ControlSwitch from "../global/control-switch.svelte";
    import ChartPlaceholder from '../global/chart-placeholder.svelte';

    // // import utils
	import { formatMonth } from '../../utils/format-dates';

    // props
    let loaded : boolean = false;
    export let once : boolean;
    export let copy : any[]
    export let refs : any[]
    export let captions : any[]

    // variable declaration
    let url : string = 'assets/data/EchoCh-nationwide-by_gender-or-age_group.csv'
    let data : any[]
    let dataIn : Map<any,any>
    let xKey : string = 'date'
    let yKey : string = 'value'
    let zKey : number = 0
    let tvChecked : boolean = false;
    let scenarioChecked : boolean = true;
    let medium : string = tvChecked ? 'web' : 'tv'
    let partisanship_scenario : string = scenarioChecked ? 'stringent' : 'lenient'
    const scaleRange : Function = scaleLinear();
    let start = 0
    let end = 1
    let gender = 'All'
    let age_group = 'All'
    
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

    $: medium = tvChecked ? 'web' : 'tv'
    $: partisanship_scenario = scenarioChecked ? 'stringent' : 'lenient'
    $: gender = 'All'
    $: age_group = 'All'
</script>

<div class="section section-2" use:inView={{ once }} on:enter={() => loaded = true }>
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
            <ControlSwitch 
                id='medium' 
                title='Medium'
                labels={[ 'TV', 'Web' ]}
                info='Internet or TV'
                bind:checked={ tvChecked } 
            />

            <ControlSwitch 
                id='partisanship' 
                title='Partisanship'
                labels={[ 'Lenient', 'Strict' ]}
                info='Lenient means that websites more partisan than TheGuardian.com (FoxNews.com) are counted as left (right), and CNN is counted as left-leaning. The stric definition means partisan content bounds are Slate.com (Breitbart.com) on the left (right)'
                bind:checked={ scenarioChecked } 
            />

            <div id='age-group' class='control control-menu'>
                <div class='control-title'>Age group</div>
                <select id="age-group-menu" name="age-group" bind:value={age_group}>
                    <option value='All'>All</option>
                    <option value='18-24'>18-24</option>
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
        {:else} <ChartPlaceholder row={3}/>
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
    .section-2 {
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
</style>