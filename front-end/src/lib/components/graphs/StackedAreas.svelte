<script lang="ts">
	// // node_modules
	import { LayerCake, Svg, flatten } from 'layercake';
	import { scaleTime, scaleOrdinal } from 'd3-scale'
	import { stack, stackOrderDescending } from 'd3-shape'
	import { extent } from 'd3-array'

	// // // components & molecules & atoms
	import AxisY from '$lib/components/graphs/layers/AxisY.svelte';
	import AxisX from '$lib/components/graphs/layers/AxisX.svelte';
	import AreaStacked from '$lib/components/graphs/layers/AreaStacked.svelte';
	import Caption from '$lib/components/graphs/layers/Caption.svelte';
	import AreaAnnotation from './tooltips/AreaAnnotation.svelte';

	// // // props declaration
	export let margins : Object = { top: 15, right: 10, bottom: 20, left: 45 }
	export let caption : string = '';
	export let includeCaption : boolean = true;
	export let url : string = '';
	export let dataMap : Map<any, any>
	export let categories : string[]
	export let colors : string[]
	export let rows : number[]
	export let formatter : Function
	export let yDomain : number[]
	export let xDomain : Date[]
	export let xTicks : Date[]
	export let addTickYLabel : boolean = true;
	export let formatTickY : Function = (d : number, i : number, a: number) => (
		i === a - 1 && addTickYLabel
		? `${d} minutes per person per day`
		: d
	);
	export let showAnnotation: boolean = false

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
	$: flatData = flatten(stackedData)

</script>

<div class='chart stacked-area-chart'>
	<LayerCake
		padding={margins}
		{flatData}
		data={stackedData}
		x={d => d.data.date}
		xScale={scaleTime()}
		xDomain={extent(xDomain)}
		y={[0, 1]}
		yDomain={yDomain}
		yNice={true}
		z={'key'}
		zScale={scaleOrdinal()}
		zDomain={categories}
		zRange={colors}
	>
		<Svg>
			<AxisX
				gridlines={false}
				snapTicks={false}
				tickMarks={true}
				ticks={xTicks}
				formatTick={formatter}
			/>
			<AxisY formatTick={ formatTickY } ticks={ 4 } />
			<AreaStacked />
			{#if showAnnotation}
				<AreaAnnotation />
			{/if}
		</Svg>
	</LayerCake>
</div>
{#if includeCaption}
	<Caption { caption } { url } type={'single-cols'} />
{/if}



<style lang='scss'></style>
