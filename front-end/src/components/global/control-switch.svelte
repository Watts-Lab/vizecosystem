<script lang='ts'>
  // property declaration
  export let id : string = '';
  export let title : string = 'Title'
  export let labels : string[] = [ 'False', 'True' ]
  export let info : string = ''
  export let checked : boolean = true;
  export let colors : string[] = ['#555', '#ccc']

  $: showInfo = false;
  $: infoDetail = showInfo ? 'active' : '';
</script>

<div id='{ id }' class='control control-switch'>
  <div class='control-title'>
    { title } 
    <span 
      class='info' 
      on:mouseenter={() => { showInfo = true }} 
      on:mouseleave={() => { showInfo =  false }}
    >?</span>
  </div>
  <div class='control-label {!checked ? 'active' : ''}'>{ labels[0] }</div>
  <label class='switch'>
    <input type="checkbox" id="medium" name="medium" bind:checked={checked}>
    <span class="slider" style='--colorFalse: {colors[0]}; --colorTrue: {colors[1]}'></span>
  </label>
  <div class='control-label {checked ? 'active' : ''}'>{ labels[1] }</div>
  <div class='info-detail {infoDetail}'>{ info }</div>
</div>

<style lang="scss">
#medium {
  grid-area: one;
}

#politicalLean {
  grid-area: one;
}

#partisanship {
  grid-area: two;
}

#diet {
  grid-area: three;
}

.control-switch {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  position: relative;
  
  .control-title {
    width: 100%;
    @include fs-xxs;
    font-weight: 300;
    letter-spacing: 1px;
    text-transform: uppercase;

    .info {
      background-color: $off-white;
      display: inline-block;
      width: 12px;
      border-radius: 100%;
      text-align: center;
      cursor: pointer;
      @include fs-xs;
    }
  }

  .control-label {
    @include fs-sm;
  }
  .control-label.active {
    text-decoration: underline;
  }

  .info-detail {
    position: absolute;
    padding: 2px 5px;
    background-color: $off-white;
    display: none;
    top: 15.5px;
    left: 0;
    right: 12.5%;
    @include fs-sm;
    z-index: 100;
  }

  .info-detail.active {
    display: block;
  }
}

/* The switch */
$switch-width: 35px;
$switch-height: 24px;

.switch {
  position: relative;
  display: inline-block;
  width: $switch-width;
  height: $switch-height;

  input {
    opacity: 0;
    width: 0;
    height: 0;
  }
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--colorTrue);
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: var(--colorFalse);
}

input:focus + .slider {
  box-shadow: 0 0 1px var(--colorFalse);
}

input:checked + .slider:before {
  -webkit-transform: translateX(11px);
  -ms-transform: translateX(11px);
  transform: translateX(11px);
}
</style>