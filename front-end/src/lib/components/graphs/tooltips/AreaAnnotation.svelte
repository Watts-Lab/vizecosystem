<script lang="ts">
    // node_modules
	import { getContext } from 'svelte';
    import { path } from 'd3-path';
    
    const { width, height } = getContext('LayerCake')

    function curveGen(context, start, ref, end) {
        context.moveTo(start.x, start.y)
        context.bezierCurveTo(ref.x, ref.y, ref.x, ref.y, end.x, end.y)
        return context
    }

    function hide() { render = false }

    $: render = true
</script>

{#if render}
    <g>
        <foreignObject class="foreign-object" width={$width} height={$height}>
            <div class="annotation-wrapper" style="transform: translate({$width/4}px,10px)">
                <div class="annotation">
                    Across all age groups, TV news dominates online news in terms of total time spend
                    <div class='close-button' on:click={hide}></div>
                </div>
            </div>
        </foreignObject>
    </g>
    <path
        class='annotation-line' 
        d={curveGen(
            path(), 
            {x: 118, y: 65}, 
            {x: 110, y: 140}, 
            {x: 103, y: 140}
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
            max-width: 145px;
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