<script lang="ts">
	// types
	import type Author from '../../types/Authors';

	export let authors : Author[];
	$: length = authors.length;

	function handleMouseOver(e) {
		e.target.classList.add('active')
	}
	function handleMouseOut(e) {
		e.target.classList.remove('active')
	}
</script>

<div class='line'></div>
<div class='title'>Credits</div>
<div class='authors'>
	{#each authors as author, i}
		<div 
			class='author-container'
			on:mouseover={handleMouseOver}
			on:focus={handleMouseOver}
			on:mouseout={handleMouseOut}
			on:blur={handleMouseOut}
		>
			<p class='author-name'>{i === length-1 ? 'and ' : ''}{author.name}{i !== length-1 ? ',' : ''}</p>
		</div>
	{/each}
</div>

<style lang='scss'>
	.authors {
		// @include grid-mobile;
		// @include centerH;
		grid-column: 1 / span last-line;
		grid-row: 3 / span 1;
		display: flex;
		flex-wrap: wrap;
		column-gap: 5px;
		row-gap: 2px;

		@media (min-width: $bp-3) {
			// @include grid-main;
			grid-row: 3 / span 1;
			grid-column: 3 / span 5;
		}

		.author-container {
			display: inline-flex;
			align-items: baseline;
			margin: 0;
			position: relative;

			.author-name {
				font-weight: 300;
				display: inline;
				pointer-events: none;
				@include fs-xs;

				@media (min-width: $bp-3) {
					@include fs-sm;
				}
			}

			.author-name:after {
				content: ',';

				@media (min-width: $bp-3) {
					display: none;
				}
			}

			.detail {
				display: none;

				.detail-list {
					@include fs-sm;
					display: none;
					position: absolute;
					top: 100%;
					left: -5px;
					z-index: 100;
					width: 250px;
					padding: 5px;
					background-color: $white;

					.detail-list-value {
						margin-bottom: 2.5px
					}
				}

				@media (min-width: $bp-3) {
					display: block;
				}
			}
			
			.detail:before {
				content: "\25BE";
				@include fs-lg;
				line-height: 0.5;
			}
		}
	}

	.line {
		grid-row: 1 / span 1;
		grid-column: 3 / span 8;
		width: 25%;
		height: 1px;
		background-color: $black;
		margin: 10px 0;
	}
	.title {
		grid-row: 2 / span 1;
		grid-column: 3 / span 8;
		@include fs-root;
		font-weight: 700;
		margin-bottom: 5px;
		// text-transform: uppercase;
	}
</style>