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
<div class='title'>The Team</div>
<div class='authors'>
	{#each authors as author, i}
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		<div 
			class='author-container'
			on:mouseover={handleMouseOver}
			on:focus={handleMouseOver}
			on:mouseout={handleMouseOut}
			on:blur={handleMouseOut}
		>
			<div class='author-photo' style="--photo-url: url('/assets/images/{author.photo}')"></div>
			<a class='author-bio' href={author.url}>
				<p class='author-name'>{author.name}</p>
				<p class='author-desc'>{author.desc}</p>
			</a>
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
		column-gap: 10px;
		row-gap: 8px;

		@media (min-width: $bp-3) {
			// @include grid-main;
			grid-row: 3 / span 1;
			grid-column: 3 / span 8;
		}

		.author-container {
			display: inline-flex;
			// align-items: baseline;
			margin: 0;
			position: relative;
			width: 100%;
			column-gap: 5px;

			@media (min-width: $bp-1) {
				width: 32%;
			}

			.author-photo {
				width: 45px;
				height: 45px;
				background-size: cover;
				background-position: center;
				background-image: var(--photo-url);
				border-radius: 50%;
				flex-grow: 0;
				flex-shrink: 0;
			}

			.author-bio {
				display: grid;
				grid-template-columns: 1fr;
				grid-template-rows: 0.3fr 0.7fr;
				color: $black;
			}

			.author-bio:hover {
				opacity: 0.9;
			}
			
			.author-bio:visited {
				color: $black;
			}

			.author-name {
				font-weight: 500;
				display: inline;
				pointer-events: none;
				@include fs-sm;

				@media (min-width: $bp-3) {
					@include fs-root;
				}
			}
			.author-desc {
				font-weight: 300;
				display: inline;
				pointer-events: none;
				@include fs-xs;

				@media (min-width: $bp-3) {
					@include fs-sm;
				}
			}
			// .author-name:after {
			// 	content: ',';

			// 	@media (min-width: $bp-3) {
			// 		display: none;
			// 	}
			// }

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
		grid-column: 1 / span 8;
		width: 25%;
		height: 1px;
		background-color: $black;
		margin: 10px 0;
		
		@media (min-width: $bp-3) {
			grid-row: 1 / span 1;
			grid-column: 3 / span 8;
		}

	}

	.title {
		grid-column: 1 / span 8;
		@include fs-root;
		font-weight: 700;
		margin-bottom: 10px;
		// text-transform: uppercase;

		@media (min-width: $bp-3) {
			grid-row: 2 / span 1;
			grid-column: 3 / span 8;
		}
	}
</style>