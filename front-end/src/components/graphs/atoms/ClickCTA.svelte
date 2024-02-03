<script lang='ts'>
    export let message : string
</script>

<div class='cta-container'>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="24" fill="white"/>
        <path d="M8 8L12.9994 20L14.7743 14.7743L20 12.9994L8 8Z" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M15 15L19 19" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M9.55291 2.20444L8.51764 6.06814" stroke="black" stroke-width="0.75" stroke-linecap="round"/>
        <path d="M2.20445 9.5529L6.06816 8.51763" stroke="black" stroke-width="0.75" stroke-linecap="round"/>
        <path d="M3.75737 3.75735L6.5858 6.58578" stroke="black" stroke-width="0.75" stroke-linecap="round"/>
        <path d="M2.20445 6.44708L6.06815 7.48236" stroke="black" stroke-width="0.75" stroke-linecap="round"/>
        <path d="M6.44709 2.20444L7.48237 6.06814" stroke="black" stroke-width="0.75" stroke-linecap="round"/>
    </svg>
    
    <span>{message}</span>
</div>

<style lang="scss">
    .cta-container {
        display: flex;
        align-items: center; 
        justify-content: center;
    }


    svg {
        width: 30px;
        height: 30px;
    }

    span {
        @include fs-sm;
        font-weight: 300;
        margin-left: 5px;
    }
</style>