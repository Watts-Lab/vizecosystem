<script lang="ts">
  // import utils
  import { politicsMap } from "../../utils/labels";

  // prop declaration
  export let data : any[];
</script>

<div class='table-container'>
  {#each data as d, i}
    <div class={`table-wrapper table-wrapper-${d.political_lean}`}>
      <div class={`row-head row-head-${d.political_lean}`}>
        <span>{d.political_lean}</span> {politicsMap.get(d.political_lean).toLowerCase()}-leaning
      </div>
      <div class={`row-body ${d.political_lean}`}>
        <div class={`row-value row-value-program`}>{d.program}</div>
        <div class={`row-value row-value-network`}>{d.network}</div>
        <div class={`row-value row-value-audience`}>{d.value}%</div>
      </div>
    </div>
  {/each}
</div>

<style lang="scss">
  .table-wrapper {
    .row-head {
      @include fs-sm;
      line-height: 2;
      padding: 0 3px;
      font-weight: 300;

      span {
        font-weight: 700;
      }
    }

    .row-head-L {
      background-color: transparentize($css-lab-dark-blue, 0.5);
      color: $white;
    }

    .row-head-R {
      background-color: transparentize($css-lab-dark-red, 0.5);
      color: $white;
    }

    .row-body {
      display: flex;
      padding: 0 3px;

      .row-value-program {
        width: 50%;
      }
      .row-value-network {
        width: 30%;
      }
      .row-value-audience {
        width: 20%;
        text-align: end;
      }
    }
  }

  .table-wrapper:first-of-type {
    margin: 0 0 25px 0;
  }
</style>