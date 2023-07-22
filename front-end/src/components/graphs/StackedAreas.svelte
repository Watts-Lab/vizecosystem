<script lang="ts">
	// // node_modules
	import { LayerCake, Svg, flatten } from 'layercake';
	import { scaleTime, scaleOrdinal } from 'd3-scale'
	import { stack, stackOrderDescending } from 'd3-shape'

	// // // types

	// // // components & molecules & atoms
	import AxisY from './atoms/AxisY.svelte';
	import AxisX from './atoms/AxisX.svelte';
	import AreaStacked from './atoms/AreaStacked.svelte';

	// // // import utils

	// // // props declaration
	export let margins : Object = { top: 20, right: 10, bottom: 20, left: 45 }
	export let data : any[]
	export let dataMap : Map<any, any>
	export let categories : string[]
	export let colors : string[]
	export let rows : number[]
	export let formatter : Function
	export let yDomain : number[]

	$: wideData = rows.map(r => {
		const obj = {}
		const dataForThisDate = dataMap.get(r)
		if (dataForThisDate !== undefined) {
			categories.forEach(c => {
				if (dataForThisDate.has(c)) obj[c] = dataForThisDate.get(c)[0].value
			})
			return { date: new Date(r), ...obj }
		}
	}).filter(d => d !== undefined)

	$: columns = Object.keys(wideData[0]).filter(d => d !== 'date')
	$: stacker = stack().keys(columns).order(stackOrderDescending)
	$: stackedData = stacker(wideData)

</script>

<div class={`chart stacked-area-chart`}>
	<LayerCake
		padding={ margins }
		flatData={ flatten(stackedData) }
		data={ stackedData }
		x={ d => d.data.date }
		xScale={ scaleTime() }
		y={ [0, 1] }
		yDomain={ yDomain }
		z={ 'key' }
		zScale={scaleOrdinal()}
		zDomain={categories}
		zRange={colors}
	>
		<Svg>
			<AxisX
				gridlines={false}
				ticks={3}
				snapTicks={true}
				tickMarks={true}
				formatTick={formatter}
			/>
			<AxisY formatTick={ d => d } ticks={ 4 } />
			<AreaStacked />
		</Svg>
	</LayerCake>
</div>

<style lang='scss'>
	.chart-title {
		grid-column: 1 / span 12;
	}

	.chart-wrapper {
        display: grid;
        grid-template-columns: 1fr;
		row-gap: 10px;
        column-gap: 10px;
		grid-row: var(--row) / span 1;
        grid-column: 1 / span 12;

        @media (min-width: $bp-3) {
			grid-column: 7 / span var(--spanCol);
			grid-row: 4 / span 1;
        }
    }

	.legend-container {
        grid-row: var(--row) / span 1;
        grid-column: span 12;
        display: flex;
        justify-content: start;
        gap: 2.5px;
		margin: 35px 0 15px 0;

        @media (min-width: $bp-3) {
			grid-row: 3 / span 1;
            grid-column: span 6;
			margin: 15px 0;
        }

        .legend-group {
            display: flex;
            align-items: baseline;

            .legend-label {
                background-color: var(--color);
                color: white;
                padding: 2.5px 5px;
                border-radius: 3px;
                font-weight: 700;
				text-align: center;
				@include fs-sm;
            }
        }
    }

	.cluster-label {
        color: var(--color);
        font-weight: 700;
	}

	.split-cols {
        grid-template-columns: 1fr;
		grid-row: var(--row) / span 1;
        grid-column: 1 / span 12;

        @media (min-width: $bp-3) {
            grid-template-columns: 10fr 2fr;
			grid-column: 1 / span var(--spanCol);
			grid-row: 4 / span 1;
        }
    }

    .single-cols {
        grid-template-columns: 1fr;
        grid-template-rows: auto 1fr;
    }
</style>
