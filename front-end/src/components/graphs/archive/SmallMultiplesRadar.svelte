<script lang='ts'>
  // // node_modules
  // import { LayerCake, Svg, Canvas, flatten } from "layercake";
  // import { stack } from 'd3-shape'
  // import { scaleTime, scaleOrdinal } from 'd3-scale'
  import { group } from "d3-array"

  // // types

  // // components & molecules & atoms
  import RadarChart from "./RadarChart.svelte";
	
  // // import utils
  import { formatMonth } from '../../utils/format-dates';
	import colorMap from '../../utils/colors';
  import { orderMap } from '../../utils/labels'
  // import stack100Pct from '../../utils/stack-pct';

  // props
  export let data : any[];
  export let flatData : any[];
  export let xKey : string = 'date';
	export let yKey : string = 'value';
	export let zKey : number = 0
  export let formatTickX : Function = formatMonth;
  export let keyColorMap : Map<string,string> = colorMap
  export let partisanship_scenario : string;
  export let period : number;
  export let diet_threshold : number;
  export let state : {};

  // variable declaration
  let dataIn : Map<any,any>

  $: if (data) {
    dataIn = group(data, d => d.month, d => d.diet_threshold, d => d.partisanship_scenario)
  }
</script>

{#if data}
  <RadarChart 
      margins={{ top: 2, right: 2, bottom: 2, left: 2 }}
      data={ flatData }
      groupedData={
        dataIn
          .get(period)
          .get(diet_threshold)
          .get(partisanship_scenario)
          .sort((a, b) => 
            orderMap.get(`${a.medium}_${a.political_lean}`) - orderMap.get(`${b.medium}_${b.political_lean}`)
          )
        }
      { yKey } 
      { xKey } 
      { zKey }
      { state }
      spanCol={12}
      customClass={ 'chart-mini' }
      formatTickX={ formatMonth }
      includeCaption={ false }
      includeAxis={ false }
      includeLabels={ false }
      on:openPopup
  />
  {:else} <div class='chart-placeholder'></div>
{/if}
