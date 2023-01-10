<!--
  @component
  Generates an SVG radial scale, useful for radar charts.
 -->
 <script>
  // node_modules
  import { getContext } from 'svelte';


  const { data, width, height, xScale } = getContext('LayerCake');

  /** @type {Number} [lineLengthFactor=1.1] - How far to extend the lines from the circle's center. A value of `1` puts them at the circle's circumference. */
  export let lineLengthFactor = 1.1;

  /** @type {Number} [labelPlacementFactor=1.25] - How far to place the labels from the circle's center. A value of `1` puts them at the circle's circumference. */
  export let labelPlacementFactor = 1.25;

  /**  @type {Number} [fillOpacity=0.5] The radar's fill opacity. */
  export let fillOpacity = 0

  /**  @type {Number} [angleOffset=Math.PI / 4] Offset by 45deg. */
  export let angleOffset = Math.PI / 4

  export let includeAxis = true;
  export let includeLabels = true;

  $: max = $xScale.range()[1];

  // $: lineLength = max * lineLengthFactor;
  // $: labelPlacement = max * labelPlacementFactor;

  $: angleSlice = (Math.PI * 2) / $data.length;

  function anchor (total, i) {
    if (i === 0 || i === total / 2) {
      return 'middle';
    } else if (i < total / 2) {
      return 'start';
    }
    return 'end';
  }
  
</script>

<g
  class='axis'
  transform="translate({ $width / 2 }, { $height / 2 })"
>
  <circle
    cx="0"
    cy="0"
    r="{max}"
    stroke="#ccc"
    stroke-width="0.5"
    fill="#CDCDCD"
    fill-opacity={fillOpacity}
  ></circle>
  <circle
    cx="0"
    cy="0"
    r="{max / 2}"
    stroke="#ccc"
    stroke-width="0.5"
    fill="none"
  ></circle>


  <!-- {#each $data as label, i}
    {@const thisAngleSlice = angleSlice * i - Math.PI / 2 + angleOffset}
    {#if includeAxis}
      <line
        x1="0"
        y1="0"
        x2="{lineLength * Math.cos(thisAngleSlice)}"
        y2="{lineLength * Math.sin(thisAngleSlice)}"
        stroke="#ccc"
        stroke-width="1"
        fill="none"
      >
      </line>
    {/if}
    {#if includeLabels}
      <text
        class='axis-label'
        text-anchor="{anchor($data.length, i)}"
        dy="0.35em"
        font-size="12px"
        text-outline="#fff"
        transform="translate({(labelPlacement) * Math.cos(thisAngleSlice)}, {labelPlacement * Math.sin(thisAngleSlice)})"
      >
        {`${label.political_lean}`}
      </text>
    {/if}
  {/each} -->
  </g>
  <!-- {#if includeLabels}
    {#each [$data[0], $data[2]] as label, i}
      <text
        class='axis-label medium-label'
        y={i * $height}
        dy={i * 7}
        x={$width / 2}
      >
        {label.medium}
      </text>
    {/each}
  {/if} -->


<style lang="scss">
  .axis-label {
    @include fs-xxs;
  }

  .medium-label {
    text-anchor: middle;
    text-transform: uppercase;
  }
  
</style>