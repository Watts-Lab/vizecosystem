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
    import ControlSwitch from "../global/control-switch.svelte";

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
            <ControlSwitch 
                id='medium' 
                title='Medium'
                labels={[ 'TV', 'Web' ]}
                info='Internet or TV'
                bind:checked={ tvChecked } 
            />
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
        grid-column: 1 / span 3;
    }
</style>