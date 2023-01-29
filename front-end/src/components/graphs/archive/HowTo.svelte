<!-- <script lang='ts'>
  // node_modules
  import { group } from "d3-array"

  // components
  import RadarChart from "./RadarChart.svelte";

  // utils
  import { formatMonth } from '../../utils/format-dates';
	import colorMap from '../../utils/colors';
  import { orderMap } from '../../utils/labels'

  export let flatData : any[];
  export let xKey : string = 'date';
	export let yKey : string = 'value';
	export let zKey : number = 0
  export let formatTickX : Function = formatMonth;
  export let keyColorMap : Map<string,string> = colorMap
  export let partisanship_scenario : string = 'lenient';
  export let period : number = 3;
  export let diet_threshold : number = 50;

  // variable declaration
  // let dataIn : Map<any,any>
  const dataIn : any[] = [{
      "state": "How to:",
      "year": 2015,
      "month": 3,
      "medium": "tv",
      "political_lean": "R",
      "diet_threshold": 50,
      "partisanship_scenario": "lenient",
      "value": 10
  },
  {
      "state": "How to:",
      "year": 2015,
      "month": 3,
      "medium": "online",
      "political_lean": "R",
      "diet_threshold": 50,
      "partisanship_scenario": "lenient",
      "value": 15
  },
  {
      "state": "How to:",
      "year": 2015,
      "month": 3,
      "medium": "online",
      "political_lean": "L",
      "diet_threshold": 50,
      "partisanship_scenario": "lenient",
      "value": 7
  },
  {
      "state": "How to:",
      "year": 2015,
      "month": 3,
      "medium": "tv",
      "political_lean": "L",
      "diet_threshold": 50,
      "partisanship_scenario": "lenient",
      "value": 20
  }]

  // $: if (data) {
  //   dataIn = group(data, d => d.month, d => d.diet_threshold, d => d.partisanship_scenario)
  //   console.log(          dataIn
  //           .get(period)
  //           .get(diet_threshold)
  //           .get(partisanship_scenario))
  // }
</script>

{#if dataIn}
  <div class='how-to'>
    <div class='how-to-label'>How to read this chart</div>
    <div class='how-to-wrapper'>
      <RadarChart 
        margins={{ top: 15, right: 15, bottom: 15, left: 15 }}
        data={ flatData }
        groupedData={
          dataIn
            .sort((a, b) => 
              orderMap.get(`${a.medium}_${a.political_lean}`) - orderMap.get(`${b.medium}_${b.political_lean}`)
            )
          }
        { yKey } 
        { xKey } 
        { zKey }
        spanCol={12}
        customClass={'chart-mini'}
        formatTickX={formatMonth}
        includeCaption={false}
        includeAxis={true}
      />
    </div>
  </div>
{/if} -->

<script lang='ts'>
  // node_modules
  import { onMount } from "svelte";

  let h : number;
  let w : number;

  onMount(() => {
    const { offsetWidth, offsetHeight } = document.getElementsByClassName('how-to-wrapper')[0]

    h = offsetHeight
    w = offsetWidth
  })
</script>

<style lang="scss">
  .how-to {
    flex-grow: 1;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;

    .how-to-wrapper {
      flex-grow: 1;
      flex-shrink: 0;
    }
    // grid-row: 1 / span 2;
    // grid-column: 7 / span 4;
    // display: grid;
    // grid-template-rows: auto 1fr;
    // gap: 15px;

    // .how-to-label {
    //   grid-row: 1 / span 1
    // }

    // .how-to-wrapper {
    //   grid-row: 2 / span 1;

    //   svg {
    //     height: 100%;
    //     width: 100%;
    //   }
    // }
  }
</style> 

<div class='how-to'>
  <div class='how-to-wrapper'>
    {#if w && h}
      <svg id="Layer_1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 308.8 208" width={w} height={h} preserveAspectRatio="xMinYMin meet">
        <style type="text/css">
          .st0{display:none;}
          .st1{display:inline;fill:none;stroke:#CCCCCC;stroke-width:0.5;}
          .st2{fill:#CDCDCD;fill-opacity:0;stroke:#CCCCCC;stroke-width:0.5;}
          .st3{fill:none;stroke:#CCCCCC;stroke-width:0.5;}
          .st4{opacity:0.8;fill:#CCCCCC;}
          .st5{opacity:0.8;fill:none;stroke:#000000;}
          .st6{fill:none;stroke:#000000;}
          .st7{fill:none;stroke:#000000;stroke-dasharray:1.9683,1.9683;}
          .st8{fill:#F7C59F;}
          .st9{fill:none;stroke:#F7934C;stroke-width:1.5;}
          .st10{fill:#C5CEB6;}
          .st11{fill:none;stroke:#588157;stroke-width:1.5;}
          .st12{stroke:#FFFFFF;stroke-width:2;}
          .st13{font-family:'Ubuntu';}
          .st14{font-size:12px;}
          .st15{fill:none;stroke:#FFFFFF;stroke-width:2;}
          .st16{font-family:'Ubuntu-Medium';}
          .st17{font-size:14.5044px;}
          .st18{fill:none;}
        </style>
       <g id="Layer_1">
        <g>
          <circle class="st2" cx="100.4" cy="103.6" r="82.2"/>
          <circle class="st3" cx="100.4" cy="103.6" r="41.1"/>
          <g class="st0">
            <polyline class="st1" points="100.4,106.8 100.4,103.6 100.4,100.5 			"/>
            <polyline class="st1" points="103.5,103.6 100.4,103.6 97.3,103.6 			"/>
          </g>
          <g>
            <polygon class="st8" points="144,147.2 100.4,103.6 80.1,124 			"/>
            <path class="st9" d="M144,147.2L80.1,124"/>
          </g>
          <g>
            <polygon class="st10" points="42.3,45.5 100.4,103.6 129.5,74.6 			"/>
            <path class="st11" d="M42.3,45.5l87.2,29.1"/>
          </g>
          <g>
            <text transform="matrix(1 0 0 1 136.1879 94.2083)" class="st12 st13 st14">10</text>
            <text transform="matrix(1 0 0 1 136.1879 94.2083)" class="st13 st14">10</text>
          </g>
          <g>
            <g>
              <text transform="matrix(1 0 0 1 167.0502 73.9111)" class="st15 st13 st14">20% of adults</text>
            </g>
            <text transform="matrix(1 0 0 1 167.0502 73.9111)" class="st13 st14">20% of adults</text>
          </g>
          <text transform="matrix(1 0 0 1 17.0067 33.0817)" class="st16 st17">Left</text>
          <text transform="matrix(1 0 0 1 146.5807 33.0817)" class="st16 st17">Right</text>
          <text transform="matrix(1 0 0 1 93.1278 55.8357)" class="st16 st17">tv</text>
          <text transform="matrix(1 0 0 1 86.282 158.4817)" class="st16 st17">web</text>
        </g>
        <rect x="199.8" y="122.3" class="st18" width="107.5" height="55.6"/>
        <text transform="matrix(1 0 0 1 199.8143 132.479)"><tspan x="0" y="0" class="st13 st14">Share of the adult</tspan><tspan x="0" y="14.4" class="st13 st14">population whose</tspan><tspan x="0" y="28.8" class="st13 st14">web news diet is </tspan><tspan x="0" y="43.2" class="st13 st14">biased to the right </tspan></text>
        <line class="st6" x1="149.6" y1="146.2" x2="195.8" y2="129.4"/>
        <g>
          <path class="st7" d="M138.3,147.2c0-3.1,2.5-5.6,5.6-5.6c7.5,0.3,7.5,11,0,11.3C140.9,152.9,138.3,150.3,138.3,147.2L138.3,147.2z
            "/>
        </g>
      </g>
      <g id="Layer_2" class="st0">
      </g>
        </svg>   
    {/if}
  </div>
</div>