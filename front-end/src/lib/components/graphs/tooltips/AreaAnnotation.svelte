<script lang="ts">
    // node_modules
	import { getContext } from 'svelte';
    import { path } from 'd3-path';

    // utils
    import getBrowserInfo from "$lib/utils/system-info";
    
    const { width, height } = getContext('LayerCake')

    function curveGen(context, start, ref, end) {
        context.moveTo(start.x, start.y)
        context.bezierCurveTo(ref.x, ref.y, ref.x, ref.y, end.x, end.y)
        return context
    }

    function hide() { render = false }

    $: render = true
    $: browserInfo = getBrowserInfo()
    $: dy = (browserInfo === 'Chrome') || (browserInfo === 'Firefox') ? 10 : 25
    $: dx = (browserInfo === 'Chrome') || (browserInfo === 'Firefox') ? 0 : 40
</script>

{#if render}
    <g>
        <foreignObject class="foreign-object" width={$width} height={$height}>
            <div class="annotation-wrapper" style="transform: translate({dx + $width/2}px, {dy}px)">
                <div class="annotation">
                    Select from different demographics such as state, age, and race to see news consumption patterns among the US population
                    <div class='close-button' on:click={hide}></div>
                </div>
            </div>
        </foreignObject>
    </g>
    <path
        class='annotation-line' 
        d={curveGen(
            path(), 
            {x: 200, y: 30}, 
            {x: 180, y: 30}, 
            {x: 180, y: -100}
        )}
        transform={`translate(0, 25)`}
    />
{/if}

<style lang="scss">
    .annotation-wrapper {
        width: 100%;
        height: 100%;
        position: relative;
        pointer-events: none;

        .annotation {
            @include fs-sm;
            position: absolute;
            max-width: 170px;
            background: white;
            padding: 2px 5px;
            box-shadow: 0 0 5px rgba(black, 0.2);
            pointer-events: all;
        }
  }

  .annotation-line {
    stroke: black;
    stroke-width: 1pt;
    fill: none;
  }

  .close-button {
    position: absolute;
    top: 0;
    right: 2px;
    pointer-events: all;
  }

  .close-button:after {
    content: '\2715';
    @include fs-root;
    line-height: 1;
  }
</style>