<script lang="ts">
  // import utils
  // import { politicsMap } from "../../utils/labels";

  // prop declaration
  export let data : any[];
  export let medium : string;
</script>

<div class='table-container'>
  <div class={`table-wrapper`}>
    <div class={`row-head`}>
      <div class={`row-header row-header-program`}>Program</div>
      <div class={`row-header row-header-audience`}>Audience</div>
    </div>
    {#each data.filter(d => d.value > 0) as row, i}
      <div class={`row-body`}>
        {#if medium === 'tv'}
          <div class={`row-value row-value-program`}>{row.program}</div>
          <div class={`row-value row-value-program`}>{row.network}</div>
          {:else} <div class={`row-value row-value-program`}>{row.domain}</div>
        {/if}
          <div class={`row-value row-value-audience`}>{row.value.toLocaleString()}</div>
      </div>
    {/each}
  </div>
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

    .row-head {
      display: flex;

      .row-header-program {
        width: 50%;
      }

      .row-header-audience {
        flex: 1 0 auto;
        text-align: end;
      }
    }

    // .row-head-L {
    //   background-color: transparentize($css-lab-dark-blue, 0.5);
    //   color: $white;
    // }

    // .row-head-R {
    //   background-color: transparentize($css-lab-dark-red, 0.5);
    //   color: $white;
    // }

    .row-body {
      display: flex;
      padding: 0 3px;
      line-height: 2;

      .row-value-program {
        width: 50%;
      }
      // .row-value-network {
      //   width: 30%;
      // }
      .row-value-audience {
        flex: 1 0 auto;
        text-align: end;
      }
    }

    .row-body:nth-child(even) {
      background-color: $light-grey;
    }
  }

  .table-wrapper:first-of-type {
    margin: 0 0 25px 0;
  }
</style>