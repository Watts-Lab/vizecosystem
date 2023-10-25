<script lang="ts">
    export let index: number;
    export let comp: any;
    export let modal: any;
</script>

<div class='option section-{index+1}' on:click={() => modal = comp}>
    <div class='option-img' style='background-image: url("{comp.image}")'></div>
    <h4>{comp.title}</h4>
</div>

<style lang='scss'>
    .option {
        grid-column: span 12;
        min-height: 100px;
        display: flex;
        flex-wrap: wrap;
        align-content: flex-start;
        row-gap: 10px;
        border: 0.5pt solid $light-grey;
        box-shadow: rgba(0, 0, 0, 0.15) 1px 1px 2px;
        padding: 7.5px;

        @media (min-width: $bp-3) {
			grid-column: span 6;
		}

        .option-img {
            height: 100%;
            width: 200px;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;

            @media (min-width: $bp-3) {
                height: 300px;
                width: 100%;
                background-size: contain;
            }
        }

        
    }
</style>