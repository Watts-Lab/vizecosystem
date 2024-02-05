<script lang="ts">
	// // node_modules
	import { LayerCake, Svg, flatten } from 'layercake';
	import { scaleTime, scaleOrdinal } from 'd3-scale'
	import { stack, stackOrderDescending } from 'd3-shape'


	// // // components & molecules & atoms
	import AxisY from '$lib/components/graphs/layers/AxisY.svelte';
	import AxisX from '$lib/components/graphs/layers/AxisX.svelte';
	import AreaStacked from '$lib/components/graphs/layers/AreaStacked.svelte';
	import Caption from '$lib/components/graphs/layers/Caption.svelte';


	// // // props declaration
	export let margins : Object = { top: 20, right: 10, bottom: 20, left: 45 }
	export let caption : string = '';
	export let includeCaption : boolean = true;
	export let url : string = '';
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

<div class='chart stacked-area-chart'>
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
				snapTicks={false}
				tickMarks={true}
				formatTick={formatter}
			/>
			<AxisY formatTick={ d => d } ticks={ 4 } />
			<AreaStacked />
		</Svg>
	</LayerCake>
</div>
{#if includeCaption}
	<Caption { caption } { url } type={'single-cols'} />
{/if}



<style lang='scss'></style>
