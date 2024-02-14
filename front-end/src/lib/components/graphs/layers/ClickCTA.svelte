<script lang='ts'>
    export let message: string;
</script>
<g class='arrow'>
    <rect width="24" height="24" fill="none" />
    <path d="M8 8L12.9994 20L14.7743 14.7743L20 12.9994L8 8Z" stroke="black" stroke-width="1" fill="white" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M15 15L19 19" stroke="black" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/>
    <text class='cta-text' x=23 y=32>{message}</text>
</g>

<style lang="scss">
    .arrow {
        transform: scale(1.5);
    }

    .cta-text {
        @include fs-xs;
        stroke: white;
        stroke-width: 2.5px;
        paint-order: stroke;
    }
</style>