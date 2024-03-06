<script lang="ts">
    import { getContext } from 'svelte';
	import MilestoneLabel from '$lib/components/graphs/tooltips/MilestoneLabel.svelte';

    export let milestones: any[] = [];

    const { width, height, xScale } = getContext('LayerCake')
</script>

<g class="milestone-annotations">
    {#each milestones as d, i}
        {@const x = $xScale(d.date)}
        <g class="milestone-group">
            <line x1={x} x2={x} y1=0 y2={$height}></line>
            <MilestoneLabel x={x} label={d.label} idx={i} orientation={d.orientation} />
        </g>
    {/each}
</g>

<style lang='scss'>
    .milestone-group {
        line {
            stroke: $true-black;
            stroke-width: 0.5;
        }
    }
    
</style>