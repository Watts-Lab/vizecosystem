<script lang='ts'>
  export let title : string
  export let onClick
</script>

<div class='btn-container' on:click={onClick}>
  <div class='btn'>{title}
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-wrench">
      <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
    </svg>
  </div>
</div>

<style lang='scss'>
  .btn-container {
    display: inline-block;
    grid-column: 1 / span 12;
    margin: 25px 0 0 0;
    cursor: pointer;
    @include fs-sm;
  }

  .btn {
    border-radius: 3px;
    padding: 5px 7.5px;
    background-color: $light-grey;
    font-weight: 400;
    color: $dark-grey;
    display: inline-flex;
    align-items: center;
    gap: 5px;
  }

  .btn:hover {
    opacity: 0.90;
  }

  .lucide {
    width: 15px;
    height: 15px;
  }
</style>