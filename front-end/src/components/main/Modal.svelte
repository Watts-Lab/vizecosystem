<script lang='ts'>
    import data from '../../data/copy.json';
    import { fade, fly } from 'svelte/transition';

    export let comp: any;
    export let modal: any;

    const { renderer: Renderer, tag } = comp
    
    const offset: number = 84

    // calculate 
	$: top = window.scrollY
    $: height = window.innerHeight - offset;
</script>

<div 
    class='modal-wrapper' 
    in:fly={{ y: 200, duration: 1000 }} 
    out:fade
    style='--top: {top + offset}px; --height: {height}px; --offset: {offset/2}px;'
>
    <div class='modal'>
        <Renderer 
            once={ true } 
            title={data[tag].filter(d => d.type === 'title')[0]}
            body={data[tag].filter(d => d.type !== 'title')}
            refs={[]}
            chart={data[tag].filter(d => d.type === 'chart')[0].value}
            bind:modal
        />
        <div 
            class='close-button' 
            on:click={() => modal = false }
        >
            GO BACK
        </div>
    </div>
</div>

<style lang="scss">
    .modal-wrapper {
        position: absolute;
        left: 0;
        right: 0;
        top: calc(var(--top) - var(--offset));
        height: var(--height);
        z-index: 9999;
        overflow-y: auto;
        margin-bottom: 100px;

        .modal {
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            width: calc($column-width + 10px);
            background-color: $white;
        }
    }

    .close-button {
        position: absolute;
        top: 15px;
        right: 0;
        padding: 0.5em;
        cursor: pointer;
        @include fs-md;
    }

    .close-button:hover {
        opacity: 0.85;
    }

    .close-button:after {
        content: '\2715';
        line-height: 1;
        margin-left: 5px;
    }
</style>