<script lang='ts'>
  // // node_modules
  // import { LayerCake, Svg, Canvas, flatten } from "layercake";
  // import { stack } from 'd3-shape'
  // import { scaleTime, scaleOrdinal } from 'd3-scale'
  import { group } from "d3-array"

  // // types

  // // components & molecules & atoms
  import LineAreaChart from "../graphs/LineAreaChart.svelte";
  // import AxisY from './atoms/AxisY.svelte';
	// import AxisX from './atoms/AxisX.svelte';
  // import AreaStacked from './atoms/AreaStacked.svelte';
	
  // // import utils
  import { formatMonth } from '../../utils/format-dates';
	import colorMap from '../../utils/colors';
  // import stack100Pct from '../../utils/stack-pct';

  // props
  export let data : any[];
  export let flatData : any[];
  export let columns : string[];
  export let xKey : string = 'date';
	export let yKey : string = 'value';
	export let zKey : number = 0
  export let formatTickX : Function = formatMonth;
  export let keyColorMap : Map<string,string> = colorMap
  export let tvChecked : boolean = false;
  export let medium : string
  export let partisanship_scenario : string;

  // variable declaration
  let dataIn : Map<any,any>

  $: if (data) {
    dataIn = group(data, d => d.medium, d => d.partisanship_scenario)
  }
</script>

{#if data}
    <LineAreaChart 
        margins={{ top: 0, right: 0, bottom: 0, left: 0 }}
        data={ flatData }
        groupedData={dataIn.get(medium).get(partisanship_scenario)}
        { yKey } 
        { xKey } 
        { zKey }
        spanCol={12}
        customClass={'chart-mini'}
        formatTickX={formatMonth}
        includeCaption={false}
        includeAxis={false}
    />
{:else} <div class='chart-placeholder'></div>
{/if}

<!-- {#if stackedData && stackedData.length} -->
  <!-- <LayerCake
    flatData = { data }
    data = { groups(groupedData, d => d.political_lean, d => d.diet_threshold) }
    x={ xKey }
    xScale={ xKey === 'date' ? scaleTime() : scaleLinear() }
    y={ yKey }
    { yDomain }
    yNice={ true }
    z={ zKey }
    zScale={ scaleOrdinal() }
    zDomain={ seriesNames }
    zRange={ seriesColors }
  > -->
  <!-- <LayerCake
    flatData={ flatten(stackedData) }
    data={ stackedData }
    x={ d => d.data[xKey] }
    xScale={ scaleTime() }
    y={ yKey }
    zScale={ scaleOrdinal() }
    z={ zKey }
    { zRange }
    zDomain={ columns }
  >
    <Svg> -->
      <!-- <AxisX
        gridlines={false}
        ticks={3}
        snapTicks={true}
        tickMarks={true}
        formatTick={formatter}
      />
      <AxisY gridlines={ false } formatTick={ d => d } /> -->
      <!-- <AreaStacked /> -->
    <!-- </Svg>
  </LayerCake> -->
<!-- {/if} -->
