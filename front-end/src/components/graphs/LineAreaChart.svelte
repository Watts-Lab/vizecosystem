<script lang="ts">
	// node_modules
	import { LayerCake, Svg, flatten } from 'layercake';
	import { scaleOrdinal, scaleTime, scaleLinear } from 'd3-scale'
	import { groups } from 'd3-array'
	import { color } from 'd3-color'

	// types
	import type Row from '../../types/TimeSeriesRow';

	// components & molecules & atoms
	import Multiline from './atoms/MultilineArea.svelte';
	import AxisX from './atoms/AxisX.svelte';
	import AxisY from './atoms/AxisY.svelte';
	import Caption from './atoms/Caption.svelte';

	// import utils
	import { politicsMap as colorMap } from '../../utils/colors';

	// props declaration
	export let margins : Object = { top: 20, right: 10, bottom: 20, left: 45 }
	export let caption : string
	export let data : Row[];
	export let url : string = '';
	export let groupedData : any[];
	export let xKey : string;
	export let yKey : string;
	export let zKey : number;
	export let yDomain : number[] = [0, null];
	export let formatTickX : Function;
	export let xTicks : number|Array<number>|Function = 6;
	export let formatTickY : Function = (d : number) => d.toLocaleString('en-NZ', { style: 'percent' });
	export let includeCaption : boolean = true;
	export let spanCol : number
	export let customClass : string
	export let includeAxis : boolean = true
	export let scaleRange : Function;
	export let start : number;
	export let end : number;


	// variable declaration
	let seriesNames = customClass === 'popup-overlay'
	? Array.from(colorMap).map(d => d[0])
	: flatten(Array.from(colorMap)
		.map(d => d[0])
		.map(d => {
			if (d === 'R') return [`${d}_1`, `${d}_0`]
			return [`${d}_0`, `${d}_1`]
		})
	)
	let seriesColors = customClass === 'popup-overlay'
	? Array.from(colorMap).map(d => d[1])
	: flatten(Array.from(colorMap).map(d => d[1]).map(d => [d, color(d).brighter(3).formatHex()]))

	$: minDate = scaleRange(start)
	$: maxDate = scaleRange(end)
</script>

<div class="chart line-chart {customClass}">
	{#if data && data.length}
		<LayerCake
			padding={ margins }
			flatData = { data.filter(d => +d.date >= minDate && +d.date <= maxDate) }
			data = { 
				groups(
					groupedData.filter(d => +d.date >= minDate && +d.date <= maxDate), 
					d => `${d.political_lean}_${d.idx}`, 
					d => d.diet_threshold
				) 
			}
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
				{/if}
				<Multiline activeChart={'test'}/>
			</Svg>
		</LayerCake>
	{/if}
</div>
{#if includeCaption}
	<Caption { caption } { url } type={spanCol === 12 ? 'split-cols' : 'single-cols'} />
{/if}
