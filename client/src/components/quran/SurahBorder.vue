<template>
    <div class="border-container">
        <svg class="border-ornament" viewBox="0 0 900 80" xmlns="http://www.w3.org/2000/svg"
            preserveAspectRatio="xMidYMid meet">

            <!-- Left line (stops before center) -->
            <line x1="40" y1="40" x2="380" y2="40" stroke="var(--color-active)" stroke-width="1.5" />

            <!-- Right line (starts after center) -->
            <line x1="520" y1="40" x2="880" y2="40" stroke="var(--color-active)" stroke-width="1.5" />
            <!-- Left ornament -->
            <g transform="translate(40,40) scale(2)">
                <path d="M 0,-10 L 10,0 L 0,10 L -10,0 Z" fill="var(--color-bg)" stroke="var(--color-active)"
                    stroke-width="0.5" transform="translate(10,0)" />

                <path d="M 0,-6 L 6,0 L 0,6 L -6,0 Z" fill="var(--color-bg)" stroke="var(--color-active)"
                    stroke-width="0.5" />
            </g>


            <!-- Right ornament -->
            <g transform="translate(870,40) scale(2)">
                <path d="M 0,-10 L 10,0 L 0,10 L -10,0 Z" fill="var(--color-bg)" stroke="var(--color-active)"
                    stroke-width="0.5" transform="translate(-10,0)" />

                <path d="M 0,-6 L 6,0 L 0,6 L -6,0 Z" fill="var(--color-bg)" stroke="var(--color-active)"
                    stroke-width="0.5" />
            </g>

        </svg>


        <div class="surahName">{{ surahName }}</div>
    </div>
</template>

<script>
export default {
    name: 'SurahBorder',
    props: {
        surahName: { type: String, required: true },
    },
};
</script>
