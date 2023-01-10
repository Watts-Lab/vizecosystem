<script lang='ts'>
  import { getContext, onMount, afterUpdate } from 'svelte';
  import { draw, scale } from 'svelte/transition';
  import { path } from 'd3-path'
  import { line, curveNatural } from 'd3-shape'
  import { group } from 'd3-array'
  import SVGPathCommander from 'svg-path-commander';

  const { custom, width, height } = getContext('LayerCake');

  const { nodes, links } = $custom;

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

  // pre-calculate positions for each object
  const dataIn : any[] = nodes.map((d : any, i : number) => {
    let x : number;
    let y : number;
    let r : number;

    if (d.node < 9) {
      x = $width / 2 + outerRadius * Math.cos(angleSlice * i - (Math.PI / 2) - angleOffset)
      y = (1 + Math.sin(angleSlice * i - (Math.PI / 2) - angleOffset)) * outerRadius
      r = d.population_size / (1 + 4 * Math.random())      
    }
    else {
      r = 20
      x = $width / 2
      y = $height - r
    }

    return { ...d, x, y, r }
  })

  const positionMap : Map<any,any> = new Map(dataIn.map(d => [d.node.toFixed(0), d]))

  const linksFromMap : Map<any,any> =  group(links, (d : any) => d.from)

  function pathGen(context, pos) {
    context.moveTo(pos.from.x, pos.from.y);
 
    if (pos.link.to === '9') {
      const ctrX = pos.from.x > $width / 2 ? $width : 0
      context.quadraticCurveTo(ctrX, $height / 1.5, pos.to.x, pos.to.y);
    }
    else if (Math.abs(+pos.link.to - +pos.link.from) === 1) {
      context.lineTo(pos.to.x, pos.to.y);
    }
    else {
      context.quadraticCurveTo($width / 2, 0.1 + Math.random() * $height, pos.to.x, pos.to.y);
    }
    
    return context;
  }

  const lineGen = line().x(d => d.x).y(d => d.y).curve(curveNatural)

  function handleMouseEnter(ev, details) {
    // select parent group
    const linkGroup = document.getElementById('link-group');

    // select connections
    const linkFrom = document.getElementsByClassName(`linkFrom-${details.node}`);
    const arrowFrom = document.getElementsByClassName(`arrowFrom-${details.node}`);
    const linkTo = document.getElementsByClassName(`linkTo-${details.node}`);
    const arrowTo = document.getElementsByClassName(`arrowTo-${details.node}`);

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
  }

  function handleMouseLeave(ev, details) {
    // select connections
    const linkFrom = document.getElementsByClassName(`linkFrom-${details.node}`);
    const arrowFrom = document.getElementsByClassName(`arrowFrom-${details.node}`);
    const linkTo = document.getElementsByClassName(`linkTo-${details.node}`);
    const arrowTo = document.getElementsByClassName(`arrowTo-${details.node}`);

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
  }

  onMount(() => render = true);
  // afterUpdate(() => actionable = true)
  
  $: render = false
  $: actionable = false
</script>


<!-- LINKS -->
<!-- transform='translate(0, {3 * $height / 8})' -->
<g class='link-group' id='link-group'>
  {#each links as link, i}
    {@const from = positionMap.get(link.from)}
    {@const to = positionMap.get(link.to)}
    {@const pathString = pathGen(path(), { from, to, link }).toString()}
    {@const totalLength = SVGPathCommander.getTotalLength(pathString)}
    {@const midpoint = SVGPathCommander.getPointAtLength(pathString, totalLength / 2)}
    {@const start = SVGPathCommander.getPointAtLength(pathString, totalLength * 0.48)}
    {@const end = SVGPathCommander.getPointAtLength(pathString, totalLength * 0.52)}

    <!-- svelte-ignore component-name-lowercase -->
    {#if render}
      <path
        class='link linkTo-{to.node} linkFrom-{from.node}'
        stroke-width={link.value}
        d={pathString}
        in:draw="{{ duration: 1000, delay: 200 + (10 * link.value) }}"
        on:introend="{() => { if (!actionable) actionable = true }}"
      ></path>
      <path
        class='arrow arrowTo-{to.node} arrowFrom-{from.node}'
        d={lineGen([start, midpoint, end])}
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
    {#each dataIn.filter(d => d.node < 9) as node, i}
      <g transform='translate({node.x}, {node.y})'>
        <circle
          class='node'
          r={node.r} 
          in:scale={{ duration: 1000 }} 
          on:mouseenter={(ev) => handleMouseEnter(ev, node)}
          on:mouseleave={(ev) => handleMouseLeave(ev, node)}
        ></circle>
        <text class='node-label' dy={-(node.r + 3)}>{node.archetype}</text>
      </g>
    {/each}
    {#each dataIn.filter(d => d.node === 9) as node, i}
      <g transform='translate({node.x}, {node.y})'>
        <circle
          class='node'
          r={node.r} 
          in:scale={{ duration: 1000 }} 
          on:mouseenter={(ev) => handleMouseEnter(ev, node)}
          on:mouseleave={(ev) => handleMouseLeave(ev, node)}
        ></circle>
        <text class='node-label' dy={node.r + 18}>{node.archetype}</text>
      </g>
    {/each}
  </g>
{/if}

<style lang="scss">
  .node {
    stroke: none;
    fill: $css-lab-dark-red;
  }

  .node-label {
    text-anchor: middle;
  }

  .link {
    fill: none;
    stroke: gainsboro;
    opacity: 0.5;
  }

  .linkTo {
    stroke: cyan;
    opacity: 0.85;
  }

  .linkFrom {
    stroke: salmon;
    opacity: 0.85;
  }

  .arrow {
    fill: none;
    stroke: black;
    stroke-width: 0.5px;
    opacity: 0;
  }

  .arrowVisible {
    opacity: 1;
  }
</style>