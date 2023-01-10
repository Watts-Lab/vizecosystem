<script lang="ts">
	// node_modules
	import { onMount } from 'svelte';
	import { LayerCake, Svg } from 'layercake';

	// types
	import type Row from '../../types/TimeSeriesRow';

	// components & molecules & atoms
	import Radar from './atoms/Radar.svelte';
	import RadialAxis from './atoms/RadialAxis.svelte';

	// import utils
	// import { politicsMap as colorMap } from '../../utils/colors';
	// import labelMap from '../../utils/labels';

	// prop declaration
	export let margins : Object = { top: 15, right: 0, bottom: 15, left: 0 }
	export let data : Row[];
	export let customClass : string;

	// variable declaration
	let render : boolean = false;

	// when component is rendered, set render to true
	// this will allow the inner contents of the LayerCake
	// component to render after width/height has been set
	onMount(() => {
		render = true
	})

	// props declaration
	// export let xKey : string;
	// export let yKey : string;
	// export let zKey : number;
	// export let yDomain : number[] = [0, null];
	// export let formatTickX : Function;
	// export let xTicks : number|Array<number>|Function = 6;
	// export let formatTickY : Function = (d : number) => d.toFixed(0);
	// export let includeCaption : boolean = true;
	// export let spanCol : number;

	// export let includeAxis : boolean = true;
	// export let includeLabels : boolean = true;
	// export let angleOffset : number = Math.PI / 4
	// export let state : {}

</script>

<div class="radar-chart {customClass}">
	<LayerCake
		padding={ margins }
		{ data }
		xDomain={[0, 1]}
		xRange={({ height }) => [0, height / 2]}
	>
		{#if render}
			<Svg>
				<RadialAxis 
					includeAxis={ true } 
					includeLabels={ false } 
				/>
				<Radar { customClass }/>
			</Svg>
		{/if}
	</LayerCake>
</div>

<style lang='scss'>
	.popupOverlay {
		height: 100%;
	}
</style>
