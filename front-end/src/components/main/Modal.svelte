<script lang='ts'>
    import data from '../../data/copy.json';
    import { fade, fly } from 'svelte/transition';

    export let comp: any;

    const { renderer: Renderer } = comp

</script>

<div class='modal-wrapper' in:fly={{ y: 200, duration: 1000 }} out:fade>
    <Renderer 
        once={ true } 
        copy={data['section-one'].copy}
        refs={data['section-one'].references}
        title={data['section-one'].title}
        captions={data['section-one'].captions}
    />
</div>

<style lang="scss">
    .modal-wrapper {
        position: absolute;
        top: 100px;
        left: 50%;
        transform: translateX(-50%);
        width: $column-width * 1.1;
        background-color: $white;
        border: 1pt solid $black;
        z-index: 1000;
    }
</style>


<!--  -->