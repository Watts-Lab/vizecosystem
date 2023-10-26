<script lang='ts'>
    import data from '../../data/copy.json';
    import { fade, fly } from 'svelte/transition';

    export let comp: any;

    const { renderer: Renderer, tag } = comp
    
    const offset: number = 84

    $: top = window.scrollY

    $: height = window.innerHeight - offset
    
</script>

<div class='modal-wrapper' in:fly={{ y: 200, duration: 1000 }} out:fade style='--top: {top + offset}px; --height: {height}px'>
    <div class='modal'>
        <Renderer 
            once={ true } 
            title={data[tag].filter(d => d.type === 'title')[0]}
            body={data[tag].filter(d => d.type !== 'title')}
            refs={[]}
            chart={data[tag].filter(d => d.type === 'chart')[0].value}
        />
    </div>
</div>

<style lang="scss">
    .modal-wrapper {
        position: absolute;
        left: 0;
        right: 0;
        top: var(--top);
        height: var(--height);
        background-color: $white;
        z-index: 9999;
        overflow-y: auto;
        margin-bottom: 100px;

        .modal {
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            width: $column-width;
        }
    }
</style>