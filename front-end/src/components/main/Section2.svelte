<script lang="ts">
    // node_modules
    import { onMount } from "svelte";
    import { csv } from "d3-fetch";
    import { autoType } from "d3-dsv";
	// import { timeFormat } from 'd3-time-format'
    
    // actions
    import inView from "../../actions/inView";

    // components
    // import ChartWrapper from "../graphs/archive/ChartWrapper.svelte";
    import FlowChart from '../graphs/FlowChart.svelte';
    
    // props
    let loaded : boolean = false;
    export let once : boolean;
    export let copy : any[];
    export let refs : any[];
    export let captions : any[];

    // variable declaration
    let url_nodes : string = 'assets/data/nodes.csv'
    let nodes : any[]
    let url_links : string = 'assets/data/links.csv'
    let links : any[]

    onMount(async () => {
        // load nodes and assign to global variable
        const nodesRes = await csv(url_nodes, autoType)
        nodes = nodesRes.map(d => ({ ...d }))
        // load links, parse into long format, assign to global variable
        const linksRes = await csv(url_links, autoType)
        links = linksRes.reduce((prev : any[], curr : Object) => {
            const entries = Object.entries(curr)
            const values = entries.filter(d => d[0] !== 'from' && d[1] !== null)
            const from = entries.filter(d => d[0] === 'from')[0][1].toFixed(0)
            values.forEach(d => {
                prev.push({ from, to: d[0], value: d[1] })
            })
            return prev
        }, [])
	})

</script>

<div class="section section-2" use:inView={{ once }} on:enter={() => loaded = true }>
    <div class='chart-wrapper'>
        {#if loaded && nodes && links}
            <FlowChart
                { nodes }
                { links }
                spanCol={12}
                url={ url_nodes }
                caption={captions[0].value}
                customClass='chart-large'
            />
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
    .section-2 {
        grid-template-columns: repeat(12, 1fr);
        column-gap: 0;
        grid-template-rows: auto auto auto 1fr auto auto;

        @media (min-width: $bp-3) {
            column-gap: 50px;
            grid-template-rows: auto auto auto 1fr auto;
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

    .chart-wrapper {
        grid-row: 3 / span 1;
        grid-column: 1 / span 12;
    }
</style>