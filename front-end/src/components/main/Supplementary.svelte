<script lang="ts">
    // props
    export let once : boolean;
    export let copy : any[];
    export let refs : any[];
</script>

<main id='supplementary' class='supplementary'>
    <div class="section section-supplementary">
        <h2 class="section-title">Methodology</h2>
        
        <div class='copy'>
            {#each copy as d}
                <p>
                    {d.value}
                </p>
            {/each}
        </div>

        <div class='references'>
            {#each refs as d}
                <p>
                    {d.value}
                </p>
            {/each}
        </div>
    </div>
</main>

<style lang='scss'>
    .supplementary {
        padding: 3em 0 10px 0;
        background-color: gainsboro;
    }

    .section-supplementary {
        grid-template-columns: repeat(12, 1fr);
        column-gap: 0;
        grid-template-rows: auto auto;
        margin-top: 0;
        margin-bottom: 0;

        @media (min-width: $bp-3) {
            column-gap: 50px;    
        }
    }

    .section-title {
        margin: 0 0 25px 0;
        grid-row: 1 / span 1;
        grid-column: 1 / span 12;
    }

    .copy {
        grid-column: span 12;
        grid-row: 1;

        @media (min-width: $bp-3) {
            grid-column: 1 / span 7;
        }

        p {
            @include fs-base;
        }
    }

    .references {
        grid-column: span 12;
        grid-row: 1;

        @media (min-width: $bp-3) {
            grid-column: 8 / span 4;
        }
    }
</style>