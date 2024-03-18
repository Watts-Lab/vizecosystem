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
        grid-column: span 6;
        display: flex;
        flex-wrap: wrap;
        align-content: flex-start;
        row-gap: 10px;
        border: 0.5pt solid $light-grey;
        box-shadow: rgba(0, 0, 0, 0.15) 1px 1px 2px;
        padding: 7.5px;
        cursor: pointer;

        @media (min-width: $bp-2) {
            grid-column: span 3;
        }

        @media (min-width: $bp-3) {
            grid-column: span 6;
        }

        @media (min-width: $bp-4) {
			grid-column: span 3;
		}

        .option-img {
            width: 100%;
            height: auto;
            aspect-ratio: 16 / 9;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;

            @media (min-width: $bp-2) {
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