<script lang="ts">
  // node_modules
  import { onMount } from 'svelte';
	import { LayerCake, Svg } from 'layercake';

  // components & molecules & atoms
  import FlowNodes from '$lib/components/graphs/layers/FlowNodes.svelte';
	import Caption from '$lib/components/graphs/layers/Caption.svelte';

  // props declaration
	export let margins : Object = { top: 50, right: 0, bottom: 50, left: 0 }
	export let caption : string = '';
	export let nodes : any[];
  export let links : any[];
  export let nodeSize : Map<any, any>;
  export let flatLinks : any[];
  export let url : string = '';
  export let includeCaption : boolean = true;
	export let spanCol : number
	export let customClass : string = ''

  onMount(() => {
    render = true
    setTimeout(() => {
			if (!userHasInteracted) {
				renderCta = true;
				userTakingTooLong = true;
			}
		}, 3500)
  });

  $: render = false
  $: userHasInteracted = false
	$: userTakingTooLong = false
	$: renderCta = false

</script>

<div class="chart flow-chart {customClass}">
  <LayerCake
    padding={ render ? margins : {} }
  >
    <Svg>
      <defs>
        <marker
          id="triangle"
          viewBox="0 0 10 10"
          refX="1"
          refY="5"
          markerUnits="userSpaceOnUse"
          markerWidth="10"
          markerHeight="10"
          orient="auto">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="black" />
        </marker>
      </defs>
      {#if render}
        <FlowNodes 
          {nodes} 
          {links} 
          {flatLinks} 
          netFlowMap={nodeSize} 
          bind:userHasInteracted
					bind:userTakingTooLong
					bind:renderCta
        />
      {/if}
    </Svg>
  </LayerCake>
</div>
{#if includeCaption}
	<Caption { caption } { url } type={spanCol === 12 ? 'split-cols' : 'single-cols'} />
{/if}

<style lang="scss"></style>