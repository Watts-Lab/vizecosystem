<script lang="ts">
    import { getContext, onMount } from 'svelte';

    const { containerWidth } = getContext('LayerCake');

    export let x: number;
    export let label: string;
    export let idx: number;
    export let orientation: string;

    let w: number =  0;
    let h: number = 0;    
    let myElement: any;

    $: render = false;
    $: if (render && myElement) {
        w = myElement.getBBox().width;
        h = myElement.getBBox().height;
    }

    onMount(() => {
        render = true
    });
</script>

{#if render}
    <g transform="translate({orientation === 'left' ? h - 5 : h * 2} {w - 12}) rotate(-90 {x} {h})">
        <text 
            id='label-{idx}' 
            {x}
            bind:this={myElement}
            >{label}</text>
        </g>
{/if}

<style lang='scss'>
    text {
        fill: $true-black;
        @include fs-sm;
        font-weight: 300;
        transform-box: fill-box;
        stroke: $white;
        stroke-width: 3px;
        paint-order: stroke;
    }
</style>