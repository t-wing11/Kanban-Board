<template>
    <div class="tag-container">
        <span
            :class="['tag-item', tagClasses(tag)]"
            v-for="(tag, index) in props.tag"
            :key="index">{{ tag }}</span>
    </div>
</template>

<script setup lang="ts">
    import { defineProps } from 'vue'

    const props = defineProps<{
    tag: string[]
    }>()

    function tagClasses(tag: string): string {
        switch (tag) {
            case 'urgent':
                return 'tag-urgent'
            case 'important':
                return 'tag-important'
            case 'optional':
                return 'tag-optional'
            case 'backlog':
                return 'tag-backlog'
            default:
                return ''
        }
    }

</script>