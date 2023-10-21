<script lang="ts">
	// node_modules
	import { LayerCake, Svg } from 'layercake';
	import { scaleTime, scaleLinear } from 'd3-scale'

	// types
	import type Row from '../../types/TimeSeriesRow';

	// components & molecules & atoms
	import Multiline from './atoms/Multiline.svelte';
	import AxisX from './atoms/AxisX.svelte';
	import AxisY from './atoms/AxisY.svelte';
	import Caption from './atoms/Caption.svelte';


	// props declaration
	export let caption : string;
	export let activeChart : string;
	export let data : Row[];
	export let url : string;
	export let groupedData : [];
	export let xKey : string;
	export let yKey : string;
	export let zKey : string;
	export let yDomain : number[] = [0, 100];
	export let formatTickX : Function;
	export let xTicks : number|Array<number>|Function = 6;
	export let formatTickY : Function = (d : number) => d.toFixed(0);
	export let includeCaption : boolean = true;
	export let spanCol : number
</script>

<div class="chart line-chart">
	<LayerCake
		padding={{ top: 20, right: 10, bottom: 20, left: 45 }}
		flatData = { data }
		data = { groupedData }
		x={ xKey }
		xScale={ xKey === 'date' ? scaleTime() : scaleLinear() }
		y={ yKey }
		{ yDomain }
		yNice={ true }
	>
		<Svg>
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
			<Multiline activeChart={activeChart}/>
		</Svg>

	</LayerCake>
</div>
{#if includeCaption}
	<Caption { caption } { url } type={spanCol === 12 ? 'split-cols' : 'single-cols'} />
{/if}
