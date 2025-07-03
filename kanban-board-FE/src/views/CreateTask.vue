<template>
    <form @submit.prevent="handleSubmit">
        <div class="form-group">
            <label for="title">Title</label>
            <input type="text" id="title" v-model="task.title" class="form-control" required />
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea id="description" v-model="task.description" class="form-control" required></textarea>
        </div>
        <div class="form-group">
            <label for="status">Status</label>
            <select id="status" v-model="task.status" class="form-control" required>
                <option value="todo">To Do</option>
                <option value="in-progress">In Progress</option>
                <option value="done">Done</option>
            </select>
        </div>
        <button type="submit" class="btn btn-primary">Save Task</button>
        <button type="button" class="btn btn-secondary" @click="cancel">Cancel</button>
    </form>
</template>

<script setup lang="ts">
    import type { TaskType } from '../types/Task';
    import { ref } from 'vue';
    import { defineEmits, defineProps } from 'vue';
    const props = defineProps<{
        task: TaskType;
    }>();

    const emit = defineEmits<{
        (e: 'save-task', task: TaskType): void;
        (e: 'cancel'): void;
    }>();

    const task = ref<TaskType>({ ...props.task });

    const handleSubmit = () => {
        emit('save-task', task.value);
    };

    const cancel = () => {
        emit('cancel');
    };
</script>