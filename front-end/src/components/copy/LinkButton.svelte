<script lang='ts'>
  export let title : string
  export let url : string
</script>

<div class='btn-container'>
  <!-- The MIT License (MIT)
  Copyright (c) 2013-2023 Cole Bemis -->
  <a class='btn' href={url} target="_top">{title}
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-external-link">
      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
      <polyline points="15 3 21 3 21 9"></polyline>
      <line x1="10" y1="14" x2="21" y2="3"></line>
    </svg>
  </a>
</div>

<style lang='scss'>
  .btn-container {
    display: inline-block;
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

  .feather {
    width: 15px;
    height: 15px;
  }
</style>