<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { csv } from "d3-fetch";
  	import { autoType } from "d3-dsv";
	import { group, rollup, descending, rank } from 'd3-array';
	import { scaleDiverging, scaleThreshold, scaleSqrt } from 'd3-scale';

    // utils
    import parseCopy from '$lib/utils/parse-copy';
	
    // types
	import type ChartConfig from '$lib/types/ChartConfig';

    // actions
    import inView from "$lib/actions/inView";

    // components
    import Beeswarm from '$lib/components/graphs/Beeswarm.svelte';
    import ChartPlaceholder from '$lib/components/global/chart-placeholder.svelte';

    // prop declaration
    let loaded : boolean = false;

    // local data
    import states from '$lib/data/states_centroids.json'
    import copy from '$lib/data/copy.json'
    const body: any[] = copy['echo-chambers-map']

    // chart config
    let data : any[];
    let dataMap : Map<string, any>
    let fullDataMap : Map<string, any>
    const urlChart : string  = 'assets/data/EchoCh-by_state.csv'

    onMount(async () => {
        // load data for map + line chart
        const resChart = await csv(urlChart, autoType)
        const rankVars : string[] = ['left_pct', 'right_pct', 'left_size', 'right_size']
        const ranks = rollup(
            resChart, 
            v => {
                const varObj = {}
                rankVars.forEach(r => {
                    const statesObj = {}
                    const ranked = rank(v.map(d => d[r]), descending)
                    v.forEach((d, i)=> { statesObj[d.state] = ranked[i] + 1 })
                    varObj[r] = statesObj
                })

                return varObj
            }, 
            d => d.period, 
            d => d.medium, 
            d => d.diet_threshold, 
            d => d.partisanship_scenario
        )
        data = resChart.map(d => ({ 
            ...d,
            left_pct_rk: ranks.get(d.period).get(d.medium).get(d.diet_threshold).get(d.partisanship_scenario)['left_pct'][d.state],
            right_pct_rk: ranks.get(d.period).get(d.medium).get(d.diet_threshold).get(d.partisanship_scenario)['right_pct'][d.state],
            left_size_rk: ranks.get(d.period).get(d.medium).get(d.diet_threshold).get(d.partisanship_scenario)['left_size'][d.state],
            right_size_rk: ranks.get(d.period).get(d.medium).get(d.diet_threshold).get(d.partisanship_scenario)['right_size'][d.state]
        }))

        // parse data for 
        dataMap = group(
            data,
            d => d.period,
            d => d.state,
            d => d.medium, 
            d => d.diet_threshold,
            d => d.partisanship_scenario
        )

        fullDataMap = group(
            data,
            d => d.state,
            d => d.medium, 
            d => d.partisanship_scenario
        )
        
    })

    const chartConfig : ChartConfig = {
        type: "diverging",
        rScale: scaleSqrt,
        rDomain: [1e3, 3e6],
        rRange: [8, 70],
        zScale: scaleThreshold,
        zDomain: [-0.1, -0.05, -0.01, 0.01, 0.05, 0.1],
        colorInterpolator: scaleDiverging,
        colorInterpolatorDomain: [-0.75, 0, 0.75],
        colorInterpolatorScheme: ["#011f5b", "gainsboro", "#990000"],
        colorPaletteAnchors: [-0.7, -0.35, -0.18, 0, 0.18, 0.35, 0.85]
    }

    $: politicalChecked = true
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
			</div>

			<div class='chart-wrapper'>
                {#if loaded && (data && data.length)}
                    <Beeswarm
                        { data }
                        { states }
                        { dataMap }
                        { fullDataMap }
                        activeChart={ chartConfig }
                        { politicalChecked }
                        caption={ d.value.captions }
                        tooltipCaptions={[1,2].map(d => (
                            body
                            .filter(d => d.type === 'chart')
                            [0]
                            .value
                            [`caption${d}`]
                            ))}
                            url={ urlChart }
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
	}

	.chart-wrapper {
        grid-column: 1 / span 12;
        margin-bottom: 25px;
    }

    .controls-wrapper {
        display: grid;
        grid-template-columns: 1fr auto 0.4fr;
        grid-template-rows: 1fr 1fr;
		margin-top: 25px;
        row-gap: 10px;
        column-gap: 5px;

        .spacer {
            border-right: 1pt solid $light-grey;
            grid-row: 1 / span 2;
            grid-column: 2 / span 1;
        }
    }

    #period {
        grid-row: 1 / span 1;
        grid-column: 3 / span 1;
        padding-left: 25px;

        .control-title {
            width: 100%;
            @include fs-xxs;
            font-weight: 300;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .labels {
            flex-grow: 1;
            display: flex;
            justify-content: space-between;

            .label {
                @include fs-sm;
            }
        }
    }

    .controls {
        display: flex;
        grid-column: 1 / span 1;

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
    }
</style>