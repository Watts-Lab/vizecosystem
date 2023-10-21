<script lang="ts">
    export let index: number;
    export let comp: any;
    export let modal: any;
</script>

<div class='option section-{index+1}' on:click={() => modal = comp}>
    <div class='option-img' style='background-image: url("{comp.image}")'></div>
    {comp.title}
</div>

<style lang='scss'>
    .option {
        grid-column: span 4;
        min-height: 400px;
        border: 1pt solid black;

        .option-img {
            height: 200px;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
    }
</style>