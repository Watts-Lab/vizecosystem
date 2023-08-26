<script lang="ts">
    // node_modules
    import { onMount } from "svelte";
    import { csv } from "d3-fetch";
    import { autoType } from "d3-dsv";
	import { scaleLinear } from 'd3-scale'
    import { group, extent } from 'd3-array'
    
    // actions
    import inView from "../../actions/inView";

    // components
    import FlowChart from '../graphs/FlowChart.svelte';
    import ControlSwitch from '../global/control-switch.svelte';
    import DoubleRangeSlider from "../global/double-range-slider.svelte";
    import ChartPlaceholder from '../global/chart-placeholder.svelte';

    // // import utils
	import { formatMonth } from '../../utils/format-dates';

    // import local data
    import data_copy from '../../data/copy.json'
    
    // props
    let loaded : boolean = false;
    export let once : boolean;
    export let copy : any[];
    export let refs : any[];
    export let captions : any[];
    export let title : string = 'Title'

    // variable declaration
    let url_nodes : string = 'assets/data/EchoCh-nodes.csv'
    let nodes : any[]
    let nodesMap : Map<any, any>
    let nodesIn : any[]
    
    let url_links : string = 'assets/data/EchoCh-links.csv'
    let links : any[]
    let linksMap : Map<any, any>
    let linksIn : any[]

    // scales
    const scaleRange : Function = scaleLinear();
    const scaleDate : Function = (x : any) => {
        const date = new Date(scaleRange(x))
        date.setDate(1)
        date.setHours(0, 0, 0)
        date.setMilliseconds(0)

        return +date
    }

    onMount(async () => {
        // load nodes and assign to global variable
        const nodesRes = await csv(url_nodes, autoType)
        nodes = nodesRes
            .map(d => ({ ...d, node: d.archetype, date: new Date(d.year, d.month, 1)  }))

        nodesMap = group(nodes, d => +d.date, d => d.variable)
            // .filter(d => d['year'] === 2016 && d['month'] === 1 && d.variable === sizeVar)

        const [ min, max ] = extent(Array.from(nodesMap).map(d => d[0]));
        scaleRange.range([ min, max ])

        // load links, parse into long format, assign to global variable
        const linksRes = await csv(url_links, autoType)
        links = linksRes
            .map(d => ({ 
                ...d, 
                start_date: new Date(d['start year'], d['start month'], 1), 
                end_date: new Date(d['end year'], d['end month'], 1) 
            }))
            .reduce((prev : any[], curr : Object) => {
                const entries = Object.entries(curr)
                const values = entries.filter(
                    d => !['start year', 'end year', 'start month', 'end month', 'from', 'start_date', 'end_date'].includes(d[0]) && 
                    d[1] !== null
                    )
                    const from = entries.filter(d => d[0] === 'from')[0][1]
                values.forEach(d => {
                    prev.push({ 
                        from, 
                        to: d[0], 
                        value: d[1], 
                        start_date: curr.start_date, 
                        end_date: curr.end_date 
                    })
                })
                return prev
            }, [])

        linksMap = group(links, d => +d.start_date, d => +d.end_date)

        render = true;
        start_date = scaleDate(0)
        end_date = scaleDate(1)
	})

    $: render = false
    $: sizeChecked = true
    $: sizeVar = sizeChecked ? 'sizes' : 'mins_p_person'

    $: start = 0
    $: end = 1

    $: start_date = scaleDate(start)
    $: end_date = scaleDate(end)

    $: if (render) {
        nodesIn = nodesMap.get(end_date).get(sizeVar)
        linksIn = linksMap.get(start_date).get(end_date)
    }
</script>

<div class="section section-3" use:inView={{ once }} on:enter={() => loaded = true }>
    <h1 class='section-title'>{ title }</h1>

    <div class='chart-wrapper'>
        <div class='controls'>
            <ControlSwitch 
                id='audience' 
                title={data_copy.controls["node-size"].title}
                labels={[ 'Audience', 'Consumption' ]}
                info={data_copy.controls["node-size"].description}
                bind:checked={ sizeChecked } 
            />
            {#if loaded && render}
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
        {#if loaded && render}
            <FlowChart
                nodes={ nodesIn }
                links={ linksIn }
                flatLinks={ links }
                spanCol={12}
                url={ url_nodes }
                caption={captions[0].value}
                customClass='chart-large'
            />
            {:else} <ChartPlaceholder row={1}/>
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
        {#each refs as d}
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
            grid-template-rows: auto auto auto auto 1fr;
        }
        
    }

    .chart-placeholder {
        height: 500px;
        background-color: lightgrey;
    }

    .section-title {
        border-bottom: 1pt solid black;
        margin: 0 0 25px 0;
        grid-row: 1 / span 1;
        grid-column: span 12;
    }

    .copy {
        grid-row: 3 / span 1;
        grid-column: span 12;

        @media (min-width: $bp-3) {
            grid-column: 1 / span 7;
        }
    }

    .references {
        grid-row: 6 / span 1;
        grid-column: span 12;

        @media (min-width: $bp-3) {
            grid-row: 3 / span 1;
            grid-column: span 5;
        }
    }

    .chart-wrapper {
        grid-row: 5 / span 1;
        grid-column: 1 / span 12;
    }

    .controls {
        display: flex;

        .control-switch,
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