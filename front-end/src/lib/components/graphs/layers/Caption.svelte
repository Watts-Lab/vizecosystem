<script lang='ts'>
    export let caption : string
    export let url : string
    export let type : string
</script>

<div class="caption caption-{type}">
    <p class='caption-text'>{@html caption}</p>
    <a class="download-button" href={url} download>
        Download data 
            <svg 
                xmlns="http://www.w3.org/2000/svg" 
                width="24" 
                height="24" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                stroke-width="2" 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                class="feather feather-download"
            >
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
    </a>
</div>

<style lang='scss'>
    .caption {
        line-height: 1.65;
        margin: 15px 0;
        @include fs-base;
    }

    .caption-text {
        display: block;

        :global(.line) {
            display: inline-block;
            height: 0.1px;
            width: 12.5px;
            border: 1px solid $black;
            position: relative;
            top: -2.5px;
        }

        :global(.area) {
            display: inline-block;
            height: 8px;
            width: 8px;
            background-color: $black;
        }
    }

    .download-button {
        color: $dark-grey;
        background-color: $light-grey;
        border-radius: 3px;
        padding: 2.5px 5px;
        margin: 10px 0 0 0;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    .download-button:hover {
        opacity: 0.90;
    }

    .caption-single-cols {
        grid-column: span 12;
    }

    .feather {
        width: 15px;
        height: 15px;
    }
</style>