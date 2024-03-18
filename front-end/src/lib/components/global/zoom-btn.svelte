<script lang="ts">
    export let zoomed: boolean = false;

    function onClick() {
        zoomed = !zoomed;
    }
</script>

<svg 
    xmlns="http://www.w3.org/2000/svg" 
    width="20" 
    height="20" 
    viewBox="0 0 24 24" 
    stroke-linecap="round" 
    stroke-linejoin="round" 
    class="feather feather-zoom"
    class:zoomed
    on:click={onClick}
>
    <g class='btn-wrapper'>
        {#if zoomed}
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            <line x1="8" y1="11" x2="14" y2="11"></line>
        {:else}
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            <line x1="11" y1="8" x2="11" y2="14"></line>
            <line x1="8" y1="11" x2="14" y2="11"></line>
        {/if}
    </g>
</svg>

<style lang='scss'>
    .feather {
        pointer-events: all;
        cursor: pointer;
		position: absolute;
		top: -48px;
		right: -10px;
		z-index: 100;
        border: 1px solid $dark-grey;
        border-radius: 2px;
        background-color: $off-white;
        fill: none;

        .btn-wrapper {
            stroke: $dark-grey;
            stroke-width: 1.5px;
        }
	}

    .feather:hover {
        border: 1px solid $black;

        .btn-wrapper {
            stroke: $black;
            stroke-width: 2.5px;
        }
    }

    .zoomed {
        background-color: $dark-grey;

        .btn-wrapper {
            stroke: $off-white;
        }
    }

    .zoomed:hover {
        .btn-wrapper {
            stroke: $off-white;
        }
    }
</style>