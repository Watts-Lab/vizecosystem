<script lang="ts">
    // components
    import EchoChambers from "../sections/EchoChambers1.svelte";
    import NewsConsumption from "../sections/NewsConsumption.svelte";
    import Section2 from "../sections/Section2.svelte";
    import Section3 from "../sections/Section3.svelte";
    import Option from "./Option.svelte";

    
    const sectionMapper = new Map([
        ['overall-news-consumption', { renderer: NewsConsumption }],
        ['echo-chambers-part1', { renderer: EchoChambers }],
        ['echo-chambers-part2', { renderer: EchoChambers }],
        ['changing-tv-audiences', { renderer: EchoChambers }]
    ]);

    export let tiles;

    // tiles
    const layout: any[] = tiles[0].value.map(d => ({
        title: d.title,
        image: 'https://dummyimage.com/300/000000/fec679', // d.tag
        tag: d.tag,
        renderer: sectionMapper.get(d.tag).renderer,
    }));

    export let modal: any
</script>

<div class='menu-wrapper'>
    {#each layout as comp, index}
        <Option {comp} {index} bind:modal />
    {/each}
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
</style>

<!-- [
    {
        renderer: Section1,
        image: 'http://placekitten.com/200/300',
        title: 'Overall News Consumption'
    },
    {
        renderer: Section2,
        image: 'https://dummyimage.com/300/ffffff/000000',
        title: 'Echo Chambers'
    },
    {
        renderer: Section3,
        image: 'https://placebear.com/200/300',
        title: 'Changing TV News Audiences'
    },
] -->