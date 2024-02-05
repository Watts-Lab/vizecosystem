<script lang='ts'>
  import { getContext, onMount } from 'svelte';
  import { draw } from 'svelte/transition';
  import SVGPathCommander from 'svg-path-commander';
  import { path } from 'd3-path'
  import { line, curveNatural } from 'd3-shape'
  import { scaleLinear, scaleSqrt } from 'd3-scale'
  import { extent } from 'd3-array'

  import nodesOrderMap from '$lib/utils/nodes';
  import slugify from '$lib/utils/slugify';
  import { formatPositiveNegative } from '$lib/utils/format-numbers';

  const { width, height } = getContext('LayerCake');

  // props declaration
  export let nodes : any[];
  export let links : any[];
  export let flatLinks : any[];
  export let netFlowMap : Map<string,number>;

  const scaleLineWidth = scaleLinear()
    .range([1,25])
  const scaleNodeSize = scaleSqrt()
    .range([5,25])

  // global variables
  let linksIn = [];

  // set dynamic curve size
  const outerRadius : number = $width / 1.75
  // calculate available angle & slice size
  const availableAngle : number = Math.acos(
    (2 * Math.pow(outerRadius, 2) - Math.pow($width, 2)) / 
    (2 * Math.pow(outerRadius, 2))
  )
  const angleSlice : number = availableAngle / (nodes.length - 1)
  // offset points so that circle is in the middle of slice
  const angleOffset : number = availableAngle / 2 - angleSlice / 2

  let dataIn;

  let positionMap : Map<any,any>

  // const linksFromMap : Map<any,any> =  group(links, (d : any) => d.from)

  function pathGen(context, pos) {
    context.moveTo(pos.from.x, pos.from.y);
 
    if (pos.link.to === 'No or Minimal News') {
      const ctrX = pos.from.x > $width / 2 ? $width : 0
      context.quadraticCurveTo(ctrX, $height / 1.5, pos.to.x, pos.to.y);
    }
    else if (Math.abs(+pos.link.to - +pos.link.from) === 1) {
      context.lineTo(pos.to.x, pos.to.y);
    }
    else {
      context.quadraticCurveTo($width / 2, 0.01 + Math.random() * $height, pos.to.x, pos.to.y);
    }
    
    return context;
  }

  const lineGen = line().x(d => d.x).y(d => d.y).curve(curveNatural)

  function handleMouseEnter(ev, details) {
    const slug = slugify(details.node)
    // select parent group
    const linkGroup = document.getElementById('link-group');

    // select connections
    const linkFrom = document.getElementsByClassName(`linkFrom-${slug}`);
    const arrowFrom = document.getElementsByClassName(`arrowFrom-${slug}`);
    const linkTo = document.getElementsByClassName(`linkTo-${slug}`);
    const arrowTo = document.getElementsByClassName(`arrowTo-${slug}`);

    // prepare array for element raising
    const moveList = [];

    // iterate over links, add class for color, prepare to raise to top of parent
    for (const el of linkFrom) {
      el.classList.toggle('linkFrom');
      moveList.push({
        selection: el,
      });     
    }
    for (const el of linkTo) {
      el.classList.toggle('linkTo');
      moveList.push({
        selection: el,
      });
    }
    // iterate over arrows and add visible class, prepare to raise to top of parent
    for (const el of arrowFrom) {
      el.classList.toggle('arrowVisible');
      moveList.push({
        selection: el,
      });     
    }
    for (const el of arrowTo) {
      el.classList.toggle('arrowVisible');
      moveList.push({
        selection: el,
      });
    }

    // raise elements to top of parent group
    for(const el of moveList) {
      linkGroup.appendChild(el.selection)
    }

    showTooltip = details.node;
  }

  function handleMouseLeave(ev, details) {
    const slug = slugify(details.node)
    // select connections
    const linkFrom = document.getElementsByClassName(`linkFrom-${slug}`);
    const arrowFrom = document.getElementsByClassName(`arrowFrom-${slug}`);
    const linkTo = document.getElementsByClassName(`linkTo-${slug}`);
    const arrowTo = document.getElementsByClassName(`arrowTo-${slug}`);

    // iterate over links, remove class for color
    for (const el of linkFrom) {
      el.classList.toggle('linkFrom');
    }
    for (const el of linkTo) {
      el.classList.toggle('linkTo');
    }
    // iterate over arrows and remove visible class
    for (const el of arrowFrom) {
      el.classList.toggle('arrowVisible');
    }
    for (const el of arrowTo) {
      el.classList.toggle('arrowVisible');
    }

    showTooltip = false;
  }

  onMount(() => {
    scaleNodeSize.domain(extent(nodes, d => d.value))
    scaleLineWidth.domain(extent(links, d => d.value))
    dataIn = nodes.map((d : any) => {
      const i : number = nodesOrderMap.get(d.node)
      let x : number;
      let y : number;
      const r : number = scaleNodeSize(d.value);

      if (d.node !== 'No or Minimal News') {
        x = $width / 2 + outerRadius * Math.cos(angleSlice * i - (Math.PI / 2) - angleOffset)
        y = (1 + Math.sin(angleSlice * i - (Math.PI / 2) - angleOffset)) * outerRadius
      }
      else {
        x = $width / 2
        y = $height - r
      }

      return { ...d, x, y, r }
    })

    positionMap = new Map(dataIn.map(d => [d.node, d]))

    linksIn = links.map((link, i) => {
      const from = positionMap.get(link.from)
      const to = positionMap.get(link.to)
      const pathString = pathGen(path(), { from, to, link }).toString()
      const pathInstance = new SVGPathCommander(pathString)
      const totalLength = +pathInstance.getTotalLength().toPrecision(2)
      const start = pathInstance.getPointAtLength(totalLength * 0.48)
      const midpoint = pathInstance.getPointAtLength(totalLength * 0.5)
      const end = pathInstance.getPointAtLength(totalLength * 0.52)

      return {
        ...link,
        to,
        from,
        pathString,
        pathInstance,
        totalLength,
        start,
        midpoint,
        end,
        w: scaleLineWidth(link.value),
      }
    })

    render = true
  });
  
  $: render = false;
  $: totalLinks = 0;
  $: actionable = false;
  $: showTooltip = false;

  $: {
    scaleNodeSize.domain(extent(nodes, d => d.value))
    scaleLineWidth.domain(extent(links, d => d.value))
    dataIn = nodes.map((d : any) => {
      const i : number = nodesOrderMap.get(d.node)
      let x : number;
      let y : number;
      const r : number = scaleNodeSize(d.value);

      if (d.node !== 'No or Minimal News') {
        x = $width / 2 + outerRadius * Math.cos(angleSlice * i - (Math.PI / 2) - angleOffset)
        y = (1 + Math.sin(angleSlice * i - (Math.PI / 2) - angleOffset)) * outerRadius
      }
      else {
        x = $width / 2
        y = $height - r
      }

      return { ...d, x, y, r }
    })

    positionMap = new Map(dataIn.map(d => [d.node, d]))

    linksIn = links.map((link, i) => {
      const from = positionMap.get(link.from)
      const to = positionMap.get(link.to)
      const pathString = pathGen(path(), { from, to, link }).toString()
      const pathInstance = new SVGPathCommander(pathString)
      const totalLength = +pathInstance.getTotalLength().toPrecision(2)
      const start = pathInstance.getPointAtLength(totalLength * 0.48)
      const midpoint = pathInstance.getPointAtLength(totalLength * 0.5)
      const end = pathInstance.getPointAtLength(totalLength * 0.52)

      return {
        ...link,
        to,
        from,
        pathString,
        pathInstance,
        totalLength,
        start,
        midpoint,
        end,
        w: scaleLineWidth(link.value)
      }
    })
  }

  $: if (linksIn.length > 0 && linksIn.length === totalLinks) {
    actionable = true;
  }  
</script>


<!-- LINKS -->
<!-- transform='translate(0, {3 * $height / 8})' -->
<g class='link-group' id='link-group'>
  {#each linksIn as link, i}
    {#if render}
      <!-- svelte-ignore component-name-lowercase -->
      <path
        class='link linkTo-{slugify(link.to.node)} linkFrom-{slugify(link.from.node)}'
        stroke-width={link.w}
        d={link.pathString}
        in:draw="{{ duration: 1000, delay: 100 + (50 * i) }}"
        on:introend={() => totalLinks += 1}  
      ></path>
      <path
        class='arrow arrowTo-{slugify(link.to.node)} arrowFrom-{slugify(link.from.node)}'
        d={lineGen([link.start, link.midpoint, link.end])}
        marker-end="url(#triangle)"
      ></path>
    {/if}
  {/each}
</g>

<!-- NODES -->
<!-- transform='translate(0, {3 * $height / 8})' -->
{#if render}
  <g 
    class='node-group'
  >
    {#each dataIn.filter(d => d.node !== 'No or Minimal News') as node, i}
      <g transform='translate({node.x}, {node.y})'>
        <circle
          class='node {actionable ? 'active' : ''}'
          r={node.r} 
          on:mouseenter={(ev) => handleMouseEnter(ev, node)}
          on:mouseleave={(ev) => handleMouseLeave(ev, node)}
        ></circle>
        <text class='node-label' dy={-(node.r + 3)}>{node.archetype}</text>
        {#if showTooltip}
          <text 
            class='node-tooltip {showTooltip === node.archetype ? 'active' : ''} {netFlowMap.get(node.archetype)[0].delta >= 0 ? 'positive' : 'negative'}'
            dx={(node.r + 3)}
            dy={5}
          >
            {formatPositiveNegative(netFlowMap.get(node.archetype)[0].delta)}
          </text>
        {/if}
      </g>
    {/each}
    {#each dataIn.filter(d => d.node === 'No or Minimal News') as node, i}
      <g transform='translate({node.x}, {node.y})'>
        <circle
          class='node {actionable ? 'active' : ''}'
          r={node.r}
          on:mouseenter={(ev) => handleMouseEnter(ev, node)}
          on:mouseleave={(ev) => handleMouseLeave(ev, node)}
        ></circle>
        <text class='node-label' dy={node.r + 18}>{node.archetype}</text>
        {#if showTooltip}
          <text 
              class='node-tooltip {showTooltip === node.archetype ? 'active' : ''} {netFlowMap.get(node.archetype)[0].delta >= 0 ? 'positive' : 'negative'}'
              dx={(node.r + 3)}
            >
              {formatPositiveNegative(netFlowMap.get(node.archetype)[0].delta)}
            </text>
        {/if}
      </g>
    {/each}
  </g>
{/if}

<style lang="scss">
  .node {
    stroke: none;
    fill: $dark-grey;
  }

  .active {
    pointer-events: all;
  }

  .node-label {
    text-anchor: middle;
    @include fs-sm;
  }

  .node-tooltip {
    opacity: 0;
    pointer-events: none;
    font-weight: 700;
    paint-order: stroke;
    stroke: white;
    stroke-width: 4pt;
  }
  
  .node-tooltip.positive {
    fill: $css-lab-dark-blue;
  }

  .node-tooltip.negative {
    fill: $css-lab-dark-red;
  }

  .node-tooltip.active {
    opacity: 1;
  }

  .link {
    fill: none;
    stroke: gainsboro;
    opacity: 0.5;
    pointer-events: none;
  }

  .linkTo {
    stroke: transparentize($css-lab-dark-blue, 0.1);
  }

  .linkFrom {
    stroke: transparentize($css-lab-dark-red, 0.1);
  }

  .arrow {
    fill: none;
    stroke: black;
    stroke-width: 1px;
    opacity: 0;
  }

  .arrowVisible {
    opacity: 1;
  }
</style>