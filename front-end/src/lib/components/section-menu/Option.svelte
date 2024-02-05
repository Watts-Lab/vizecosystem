<script lang="ts">
    import { base } from '$app/paths';

    export let index: number;
    export let comp: any;
</script>

<a class='option section-{index+1}' href='{base}/{comp.tag}'>
    <div class='option-img' style='background-image: url({comp.image})'></div>
    <h4>{comp.title}</h4>
</a>

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
        cursor: pointer;

        @media (min-width: $bp-3) {
			grid-column: span 6;
		}

        .option-img {
            height: 100%;
            width: auto;
            aspect-ratio: 16 / 9;
            // width: 200px;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;

            @media (min-width: $bp-3) {
                width: 100%;
                height: auto;
                background-size: contain;
            }
        }

        h4 {
            color: $dark-grey;
        }
    }

    .option:hover {
        opacity: 0.9;
    }
</style>