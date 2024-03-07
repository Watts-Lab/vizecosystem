<script lang="ts">
	// node_modules
	import { LayerCake, Svg } from 'layercake';
	import { scaleOrdinal, scaleTime, scaleLinear } from 'd3-scale'
	import { max } from 'd3-array'

	// types
	import type Row from '$lib/types/TimeSeriesRow';

	// components & molecules & atoms
	import Multiline from '$lib/components/graphs/layers/MultilineArea.svelte';
	import AxisX from '$lib/components/graphs/layers/AxisX.svelte';
	import AxisY from '$lib/components/graphs/layers/AxisY.svelte';
	import Caption from '$lib/components/graphs/layers/Caption.svelte';
	import Legend from '$lib/components/graphs/legend/MultilineAreaLegend2.svelte'
	import LineAreaAnnotation from '$lib/components/graphs/tooltips/LineAreaAnnotation.svelte';
	import Milestones from '$lib/components/graphs/tooltips/Milestones.svelte';

	// import utils
	import { politicsMap as colorMap } from '$lib/utils/colors';
	import type Milestone from '$lib/types/Milestone';
	
	// props declaration
	export let margins : Object = { top: 20, right: 10, bottom: 20, left: 45 }
	export let caption : string = ''
	export let data : Row[];
	export let url : string = '';
	export let groupedData : any[];
	export let xKey : string;
	export let yKey : string;
	export let zKey : number;
	export let yDomain : number[] = [0, null];
	export let formatTickX : Function;
	export let xTicks : number|Array<number>|Function = 6;
	export let formatTickY : Function = (d : number, i : number, a: number) => (
		i === a - 1
		? `${d.toLocaleString('en-NZ', { style: 'percent' })} of population`
		: d.toLocaleString('en-NZ', { style: 'percent' })
	);
	export let includeCaption : boolean = true;
	export let spanCol : number
	export let customClass : string
	export let includeAxis : boolean = true
	export let scaleRange : Function;
	export let start : number;
	export let end : number;
	export let displayAnnotation: boolean = false;
	export let milestones: Milestone[] = [];

	// variable declaration
	let seriesNames = customClass === 'popup-overlay'
	? Array.from(colorMap).map(d => d[0])
	: Array.from(colorMap).map(d => d[0])

	let seriesColors = customClass === 'popup-overlay'
	? Array.from(colorMap).map(d => d[1])
	: Array.from(colorMap).map(d => d[1])

	$: minDate = scaleRange(start)
	$: maxDate = scaleRange(end)

	$: console.log(data.filter(d => d.value >= 0.2))
</script>

<div class="chart-container">
	<Legend { seriesNames } { seriesColors } />
	
	<div class='chart line-chart {customClass}'>
		{#if data && data.length}
			<LayerCake
				padding={ margins }
				flatData = { data.filter(d => +d.date >= minDate && +d.date <= maxDate) }
				data = {Array.from(groupedData).map(d => [d[0], Array.from(d[1])])}
				x={ xKey }
				xScale={ xKey === 'date' ? scaleTime() : scaleLinear() }
				y={ yKey }
				{ yDomain }
				yNice={ true }
				z={ zKey }
				zScale={ scaleOrdinal() }
				zDomain={ seriesNames }
				zRange={ seriesColors }
			>
				<Svg>
					<pattern id="diagonalHatchR" patternUnits="userSpaceOnUse" width="4" height="4">
						<path d="M-1,1 l2,-2
								 M0,4 l4,-4
								 M3,5 l2,-2" 
						style="stroke:{colorMap.get('R')}; stroke-width:1.5" />
					</pattern>
					<pattern id="diagonalHatchL" patternUnits="userSpaceOnUse" width="4" height="4">
						<path d="M-1,1 l2,-2
								 M0,4 l4,-4
								 M3,5 l2,-2" 
						style="stroke:{colorMap.get('L')}; stroke-width:1.5" />
					</pattern>
					{#if includeAxis}
						<AxisX
							gridlines={false}
							ticks={xTicks}
							formatTick={formatTickX}
							snapTicks={false}
							tickMarks={true}
						/>
						<AxisY
							ticks={4}
							formatTick={formatTickY}
						/>
						<Milestones { milestones } />
					{/if}
					{#if displayAnnotation}
						<LineAreaAnnotation />
					{/if}
					<Multiline activeChart={'activeChart'} />
				</Svg>
			</LayerCake>
		{/if}
	</div>
</div>
{#if includeCaption}
	<Caption { caption } { url } type={spanCol === 12 ? 'split-cols' : 'single-cols'} />
{/if}

<style lang='scss'></style>
