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
    $: dy = (browserInfo === 'Chrome') || (browserInfo === 'Firefox') ? 80 : 105
</script>

{#if render}
    <g>
        <foreignObject class="foreign-object" width={$width} height={$height}>
            <div class="annotation-wrapper" style="transform: translate({5}px, {dy}px)">
                <div class="annotation">
                    The definition of echo chambers range from 50% (the line <span class='line'></span>) of one's news diet to 75% (the areas <span class='area'></span> below the line)
                    <div class='close-button' on:click={hide}></div>
                </div>
            </div>
        </foreignObject>
    </g>
    <path
        class='annotation-line' 
        d={curveGen(
            path(), 
            {x: 45, y: 200}, 
            {x: 37, y: 195}, 
            {x: 37, y: 155}
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
            max-width: 175px;
            background: $white;
            padding: 2px 5px;
            box-shadow: 0 0 5px rgba($black, 0.2);
            pointer-events: all;

            .line {
                display: inline-block;
                height: 1px;
                width: 12.5px;
                border: 1px solid $black;
                position: relative;
                top: -2.5px;
            }

            .area {
                display: inline-block;
                height: 10px;
                width: 10px;
                background-color: $black;
            }
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