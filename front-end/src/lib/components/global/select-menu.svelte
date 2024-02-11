<script lang='ts'>
  export let id : string = '';
  export let title : string = 'Title'
  export let value : string;
  export let options : Map<string, string>
  export let disabled : boolean = false;
</script>


<div id='{id}' class='control control-menu'>
    <div class='control-title'>{title}</div>
    <select 
        id="menu menu_{id}" 
        name="select_{id}}" 
        disabled={disabled}
        bind:value={value}
    >
        {#each Array.from(options) as d, i}
            <option value={d[0]}>{d[1]}</option>
        {/each}
    </select>
</div>

<style lang="scss">
    .control-menu {
        display: flex;
        flex-wrap: wrap;

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
            @include fs-xs;
            }
        }

        .control-label {
            @include fs-sm;
        }
        .control-label.active {
            text-decoration: underline;
        }

        select {
            margin: 0;
            @include fs-sm;
        }
    }
</style>