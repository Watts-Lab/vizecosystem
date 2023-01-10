<!--
  @component
  Generates an SVG radar chart.
 -->
 <script>
  // node_modules
  import { getContext } from 'svelte';
  import { flatten } from 'layercake';
  import { line, curveCardinalClosed, curveLinearClosed } from 'd3-shape';

  // utils
  import slugify from '../../../utils/slugify'
  import { orderMap } from '../../../utils/labels'
  import { mediumMap } from '../../../utils/colors'

  const { data, width, height, xGet, xScale, extents } = getContext('LayerCake');

  /**  @type {String} [fill='#f0c'] The radar's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let fill = '#f0c'

  /**  @type {String} [stroke='#f0c'] The radar's stroke color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let stroke = 'black'

  /**  @type {Number} [stroke=2] The radar's stroke color. */
  export let strokeWidth = 2

  /**  @type {Number} [fillOpacity=0.5] The radar's fill opacity. */
  export let fillOpacity = 0

  /**  @type {Number} [r=4.5] Each circle's radius. */
  export let r = 4.5;

  /**  @type {String} [circleFill="#f0c"] Each circle's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let circleFill = "#f0c";

  /**  @type {String} [circleStroke="#fff"] Each circle's stroke color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let circleStroke = "#fff";

  /**  @type {Number} [circleStrokeWidth=1] Each circle's stroke width. */
  export let circleStrokeWidth = 1;

  /**  @type {Number} [angleOffset=Math.PI / 4] Offset by 45deg. */
  export let angleOffset = Math.PI / 4

  /**  @type {String} [angleOffset=Math.PI / 4] Offset by 45deg. */
  export let customClass  = ''

  let path;
  let dataIn;

  $: angleSlice = Math.PI / 2;

  $: path = line()
      .curve(curveLinearClosed)
      .x(d => {
        if (d) return d.value * Math.cos(
          angleSlice * orderMap.get(`${d.medium}_${d.political_lean}`) - Math.PI / 2 + angleOffset)
        return 0;
      })
      .y(d => {
        if (d) return d.value * Math.sin(
          angleSlice * orderMap.get(`${d.medium}_${d.political_lean}`) - Math.PI / 2 + angleOffset)
        return 0;
      });
  
  $: dataIn = [
    { value: $xScale($data[0].right_pct), medium: 'tv', political_lean: 'R' },
    { value: $xScale($data[1].right_pct), medium: 'online', political_lean: 'R' },
    { value: $xScale($data[1].left_pct), medium: 'tv', political_lean: 'L' },
    { value: $xScale($data[0].left_pct), medium: 'online', political_lean: 'L' },
  ]
  
</script>

<g
  class='radar-path'
  transform="translate({ $width / 2 }, { $height / 2 })"
>
  {#if dataIn}
    <clipPath id={`clipPath-${slugify($data[0].state)}_tv_${customClass}`}>
      <path
        d='{path([ ...dataIn.filter(d => d.medium === 'tv'), false ])}'
        stroke="{stroke}"
        stroke-width="{0}"
        fill-opacity="{1}"
        fill="{mediumMap.get('tv').polygon}"
        shape-rendering="geometricPrecision"
      ></path>
    </clipPath>
    <clipPath id={`clipPath-${slugify($data[0].state)}_online_${customClass}`}>
      <path
        d='{path([ ...dataIn.filter(d => d.medium === 'online'),  false ])}'
        stroke="{stroke}"
        stroke-width="{0}"
        fill-opacity="{1}"
        fill="{mediumMap.get('online').polygon}"
        shape-rendering="geometricPrecision"
      ></path>
    </clipPath>
    
    <g class='top_bg_tv' clip-path={`url(#clipPath-${slugify($data[0].state)}_tv_${customClass})`}>
      <rect
        x={-$width / 2}
        y={-$height / 2}
        height={$height / 2}
        width={$width / 2}
        fill='blue'
        fill-opacity={0.5}
      ></rect>
      <rect
        x={0}
        y={-$height / 2}
        height={$height / 2}
        width={$width / 2}
        fill='red'
        fill-opacity={0.5}
      ></rect>
    </g>
    <g class='top_bg_tv' clip-path={`url(#clipPath-${slugify($data[0].state)}_online_${customClass})`}>
      <rect
        x={-$width / 2}
        y={0}
        height={$height / 2}
        width={$width / 2}
        fill='blue'
        fill-opacity={0.5}
      ></rect>
      <rect
        x={0}
        y={0}
        height={$height / 2}
        width={$width / 2}
        fill='red'
        fill-opacity={0.5}
      ></rect>
    </g>
  {/if}
</g>

<style>
  .path-line {
    stroke-linejoin: round;
    stroke-linecap: round;
  }
</style>

<!-- {#each $data as row} -->
    <!-- Draw a line connecting all the dots -->
    <!-- <path
      class='path-line'
      d='{path(xVals)}'
      stroke="{stroke}"
      stroke-width="{strokeWidth}"
      fill="{fill}"
      fill-opacity="{fillOpacity}"
    ></path> -->

    <!-- Plot each dots -->
    <!-- {#each xVals as circleR, i}
      {@const thisAngleSlice = angleSlice * i - Math.PI / 2}
      <circle
        cx={circleR * Math.cos(thisAngleSlice)}
        cy={circleR * Math.sin(thisAngleSlice)}
        r="{r}"
        fill="{circleFill}"
        stroke="{circleStroke}"
        stroke-width="{circleStrokeWidth}"
      ></circle>
    {/each} -->
  <!-- {/each} -->