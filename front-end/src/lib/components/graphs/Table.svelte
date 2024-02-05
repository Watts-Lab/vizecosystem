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
      <div class={`row-header row-header-program`}>{medium === 'tv' ? 'Program' : 'Domain'}</div>
      <div class={`row-header row-header-audience`}>Audience</div>
    </div>
    {#each data.filter(d => d.value > 0) as row, i}
      <div class={`row-body`}>
        {#if medium === 'tv'}
          <div class={`row-value row-value-program`}>{row.program} <p class={`row-value row-value-network`}>{row.network}</p> </div>
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
      @include fs-base;
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

    .row-body {
      display: flex;
      align-items: center;
      gap: 5px;
      padding: 3px 5px;
      line-height: 2;
      min-height: 40px;
      @include fs-base;
      border-bottom: 0.5pt solid $light-grey;

      .row-value-network {
        @include fs-sm;
        color: $dark-grey;
        font-weight: 300;
      }
      .row-value-audience {
        flex: 1 0 auto;
        text-align: end;
        align-self: flex-start;
      }
    }

    .row-body:nth-child(even) {
      background-color: transparentize($light-grey, 0.5);
    }

    .row-body:last-child {
      border-bottom: none;
    }
  }

  .table-wrapper:first-of-type {
    margin: 0 0 25px 0;
  }
</style>