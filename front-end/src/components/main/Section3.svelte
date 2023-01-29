<script lang="ts">
    // node_modules
    import { onMount } from "svelte";
    import { csv } from "d3-fetch";
    import { autoType } from "d3-dsv";
    import { group, groups } from "d3-array";

    // import types
    // import type Node from '../../types/Node'
    // import type Link from '../../types/Link'
    
    // actions
    import inView from "../../actions/inView";

    // components
    import LineChart from "../graphs/LineChart.svelte";

    // utils
    // import enforceOrder from "../../utils/order";
    import { formatPct } from '../../utils/format-numbers';
  

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
    let url : string = 'assets/data/segregation-survival.csv'
    let data : any[]
    let xKey : string = 'month'
    let yKey : string = 'value'
    let zKey : string = 'political_lean'
    let dataIn : Map<any,any>
    let tvChecked : boolean = true;
    let medium : string = tvChecked ? 'tv' : 'online'
    
    onMount(async () => {
        const res = await csv(url, autoType)
        data = res
	})

    $: if (data) { dataIn = group(data, d => d.medium ) }
    $: medium = tvChecked ? 'tv' : 'online'

</script>

<div class="section section-3" use:inView={{ once }} on:enter={() => loaded = true }>
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
    </div>
    <div class='chart-wrapper'>
        {#if loaded && data}
            <LineChart 
                data={ data }
                groupedData={
                    groups(dataIn.get(medium), d => d.medium, d => d.political_lean )
                }
                { yKey } 
                { xKey } 
                { zKey }
                formatter={formatPct(2)}
                url={ url }
                spanCol={12}
                customClass={'chart-medium'}
                tooltipType={'community'}
                caption={captions[0].value}
                title={'Survival curves'}
            />
        {:else} <div class='chart-placeholder'></div>
        {/if}
    </div>
    <div class='copy'>
        {#each copy as d, i}
            <p>
                {d.value}
            </p>
        {/each}
    </div>
    <div class='references'>
        {#each refs as d, i}
            <p>
            {d.value}
            </p>
        {/each}
    </div>
    
</div>

<style lang='scss'>
    .section-3 {
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

    .chart-wrapper {
        grid-row: 3 / span 1;
        grid-column: 1 / span 12;
    }

    .section-title {
        border-bottom: 1pt solid black;
        margin: 0 0 25px 0;
        grid-row: 1 / span 1;
        grid-column: span 12;
    }

    .copy {
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
            grid-row: 5 / span 1;
            grid-column: span 5;
        }
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