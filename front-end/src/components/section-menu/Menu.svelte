<script lang="ts">
    // components
    import EchoChambers1 from "../sections/EchoChambers1.svelte";
    import EchoChambers2 from "../sections/EchoChambers2.svelte";
    import NewsConsumption from "../sections/NewsConsumption.svelte";
    import ChangingTVAudiences from "../sections/ChangingTVAudiences.svelte";
    import Methodology from "../sections/Methodology.svelte";
    import Option from "./Option.svelte";
    import LinkMethodology from "./LinkMethodology.svelte";

    
    const sectionMapper = new Map([
        ['overall-news-consumption', { renderer: NewsConsumption }],
        ['echo-chambers-part1', { renderer: EchoChambers1 }],
        ['echo-chambers-part2', { renderer: EchoChambers2 }],
        ['changing-tv-audiences', { renderer: ChangingTVAudiences }]
    ]);
    const methodology = { tag: 'methodology', renderer : Methodology };

    export let tiles: any[];

    // tiles
    const layout: any[] = tiles[0].value.map(d => ({
        title: d.title,
        image: `/assets/images/${d.tag}.png`,
        tag: d.tag,
        renderer: sectionMapper.get(d.tag).renderer,
    }));

    export let modal: any
</script>

<div class='menu-wrapper'>
    {#each layout as comp, index}
        <Option {comp} {index} bind:modal />
    {/each}

    <!-- <div 
        class='methodology' 
        on:click={() => modal = methodology }
    >Read the methodology</div> -->
    <LinkMethodology 
        title={'Read the methodology'} 
        onClick={() => modal = methodology}
    />
</div>

<style lang="scss">
    .menu-wrapper {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(12, 1fr);
        column-gap: 10px;
        row-gap: 10px;
        margin: 0 0 50px 0;
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
