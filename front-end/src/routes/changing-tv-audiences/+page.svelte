<script lang="ts">
	// node_modules
	import { onMount } from "svelte";
    import { csv } from "d3-fetch";
    import { autoType } from "d3-dsv";
	import { scaleLinear } from 'd3-scale'
    import { group, extent } from 'd3-array'

	// actions
	import inView from "$lib/actions/inView";

	// components
	import FlowChart from '$lib/components/graphs/FlowChart.svelte';
    import DoubleRangeSlider from "$lib/components/global/double-range-slider.svelte";
    import ChartPlaceholder from '$lib/components/global/chart-placeholder.svelte';
    import ClickCta from '$lib/components/graphs/layers/ClickCTA.svelte';

	// // import utils
	import { formatMonth } from '$lib/utils/format-dates';
	import parseCopy from '$lib/utils/parse-copy';
	
	// import local data
    import copy from '$lib/data/copy.json'
    const body: any[] = copy['changing-tv-audiences']

	// prop declaration
	let loaded : boolean = false;

	// variable declaration
    let url_nodes : string = 'assets/data/EchoCh-nodes.csv'
    let nodes : any[]
    let nodesMap : Map<any, any>
    let nodesIn : any[]

    let url_nodes_size : string = 'assets/data/EchoCh-nodes-net_change_in_size.csv'
    let nodes_size : any[]
    let nodesSizeMap : Map<any, any>
    let nodeSizeIn : Map<any, any>
    
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

        nodesMap = group(nodes, d => +d.date)

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

        // load node size, parse into long format, assign to global variable
        const nodeSizeRes = await csv(url_nodes_size, autoType)
        nodes_size = nodeSizeRes
            .map(d => ({ 
                ...d, 
                start_date: new Date(d['start year'], d['start month'], 1), 
                end_date: new Date(d['end year'], d['end month'], 1) 
            }))
        nodesSizeMap = group(nodes_size, d => +d.start_date, d => +d.end_date, d => d.archetype)

        render = true;
        start_date = scaleDate(0)
        end_date = scaleDate(1)
	})

    $: render = false

    $: start = 0
    $: end = 1

    $: start_date = scaleDate(start)
    $: end_date = scaleDate(end)

    $: if (render) {
        nodesIn = nodesMap.get(end_date) //.get(sizeVar)
        linksIn = linksMap.get(start_date).get(end_date)
        nodeSizeIn = nodesSizeMap.get(start_date).get(end_date)
	}
</script>

<div class="section" use:inView={{ once: true }} on:enter={() => loaded = true }>
	{#each body as d, i}
        {#if d.type === 'text'}
            <p class='copy'>
                {@html parseCopy(d.value)}
            </p>
        {:else if d.type === 'title'} <h1 class='section-title'>{ d.value }</h1>
		{:else}
			<div class='title-container'>
				<h3 class='chart-title'>
					{d.value.title}
				</h3>
			
				<div class='controls'>
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

                <div class='block-cta'>
                    <ClickCta 
                        message={'Hover over circles to see net flow for archetype'} 
                    />
                </div>
			
				{#if loaded && render}
					<FlowChart
						nodes={ nodesIn }
						links={ linksIn }
                        nodeSize={ nodeSizeIn }
						flatLinks={ links }
						spanCol={12}
						url={ url_nodes }
						caption={d.value.captions}
						customClass='chart-flow'
					/>
					{:else} <ChartPlaceholder />
				{/if}
			</div>
		{/if}
	{/each}
</div>

<style lang='scss'>
    .section {
        grid-template-columns: repeat(12, 1fr);
        column-gap: 15px;
    }

	.section-title {
        grid-row: 1 / span 1;
        grid-column: 3 / span 8;
		margin-bottom: 1em;
    }

	.copy {
        grid-column: span 12;

        @media (min-width: $bp-3) {
            grid-column: 3 / span 8;
        }
    }

	p {
		margin-top: 0;
		margin-bottom: 1em;
		@include fs-root;

		@media (min-width: $bp-3) {
			@include fs-md;
		}
	}

    .title-container {
		grid-column: span 12;
        margin-top: 25px;

        h3 {
			margin-bottom: 1em;
		}
	}

	.chart-wrapper {
        grid-column: 1 / span 12;
        margin-bottom: 25px;
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

	.legend {
		display: flex; 
		gap: 15px;
		margin-top: 15px;
		font-size: 14px;

		.legend-item {
			display: flex;
			align-items: center;
			gap: 5px;
			
			.legend-color {
				background-color: var(--color);
				width: 17.5px;
				height: 17.5px;
				border-radius: 3px;
			}
		}
	}

    .block-cta {
        margin: 20px 0;
    }
</style>
