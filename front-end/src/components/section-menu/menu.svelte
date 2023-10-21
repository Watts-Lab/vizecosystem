<script lang="ts">
    // components
    import Section1 from "../main/Section1.svelte";
    import Section2 from "../main/Section2.svelte";
    import Section3 from "../main/Section3.svelte";
    import Option from "./option.svelte";

    // components
    const layout: any[] = [
        {
            renderer: Section1,
            image: 'http://placekitten.com/200/300',
            title: 'Overall News Consumption'
        },
        {
            renderer: Section2,
            image: 'http://placekitten.com/205/307',
            title: 'Echo Chambers'
        },
        {
            renderer: Section3,
            image: 'http://placekitten.com/210/340',
            title: 'Changing TV News Audiences'
        },
    ]

    export let modal: any
</script>

<div class='menu-wrapper'>
    {#each layout as comp, index}
        <Option {comp} {index} bind:modal />
    {/each}
</div>

<style lang="scss">
    .menu-wrapper {
        grid-row: 4 / span last-line;
        display: grid;
        grid-template-columns: repeat(12, 1fr);
        column-gap: 10px;
        margin: 0 0 50px 0;
    }
</style>