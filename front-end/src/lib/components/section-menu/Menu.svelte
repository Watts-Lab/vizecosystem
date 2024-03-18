<script lang="ts">
    // components
    import Option from "./Option.svelte";

    export let tiles: any[];

    // tiles
    const layout: any[] = tiles[0].value.map((d: any) => ({
        ...d,
        image: `assets/images/${d.tag}.png`,
    }));
</script>

<div class='menu-wrapper'>
    {#each layout as comp, index}
        <Option {comp} {index} />
    {/each}
</div>

<style lang="scss">
    .menu-wrapper {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(12, 1fr);
        column-gap: 10px;
        row-gap: 10px;
        margin: 50px auto;

        @media (min-width: $bp-2) {
            width: 80%;
        }

        @media (min-width: $bp-4) {
            width: 100%;
        }
    }

    .methodology {
        grid-column: 1 / span 12;
        margin: 25px 0 0 0;
        cursor: pointer;
        @include fs-sm;
    }

    .methodology:hover {
        opacity: 0.9;
    }
</style>
