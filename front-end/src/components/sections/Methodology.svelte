<script lang="ts">
	// actions
	import inView from "../../actions/inView";

	// prop declaration
	let loaded : boolean = false;
	export let once : boolean;
	export let body : any[];
	export let title : any;
	export let refs : string[];
	export let modal : any;
	export let chart : any;
</script>

<div class="section" use:inView={{ once }} on:enter={() => loaded = true }>
	<h1 class='section-title'>{ title.value }</h1>
	{#each body as d, i}
		{#if d.type === 'text'}
			<p class='copy'>
				{d.value}
			</p>
		{/if}
	{/each}
	<div 
		class='close-button bottom' 
		on:click={() => modal = false }
	>
		GO BACK
	</div>
</div>

<style lang='scss'>
	.section {
        grid-template-columns: repeat(12, 1fr);
        column-gap: 0;

        @media (min-width: $bp-3) {
            column-gap: 50px;
        }
    }

	.section-title {
        border-bottom: 0.5pt solid black;
        grid-row: 1 / span 1;
        grid-column: span 12;
		margin-bottom: 1em;
    }

	.copy {
        grid-column: span 12;

        @media (min-width: $bp-3) {
            grid-column: 1 / span 7;
        }
    }

	p {
		margin-top: 0;
		margin-bottom: 1em;
		@include fs-root;

		@media (min-width: $bp-3) {
			@include fs-md;
		}
	}

	.title-container {
		grid-column: span 12;

		h3 {
			margin-bottom: 1em;
		}
	}

	.controls {
        display: flex;

        .control-switch, 
        .control-menu,
        .control-range {
            display: flex;
            flex-wrap: wrap;
        
            .control-title {
                width: 100%;
                @include fs-xxs;
                font-weight: 300;
                letter-spacing: 1px;
                text-transform: uppercase;

                .info {
                background-color: $off-white;
                display: inline-block;
                width: 12px;
                border-radius: 100%;
                text-align: center;
                @include fs-xs;
                }
            }

            .control-label {
                @include fs-sm;
            }
            .control-label.active {
                text-decoration: underline;
            }

            select {
                margin: 0;
                @include fs-sm;
            }
        }
	}

	.legend {
		display: flex; 
		gap: 15px;
		margin-top: 15px;
		font-size: 14px;

		.legend-item {
			display: flex;
			align-items: center;
			gap: 5px;
			
			.legend-color {
				background-color: var(--color);
				width: 17.5px;
				height: 17.5px;
				border-radius: 3px;
			}
		}
	}

	.close-button.bottom {
		grid-column: 6 / span 2;
		text-align: center;
		cursor: pointer;
        @include fs-sm;
	}

	.close-button:hover {
        opacity: 0.85;
    }

    .close-button:after {
        content: '\2715';
        line-height: 1;
        margin-left: 5px;
    }
</style>
