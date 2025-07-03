<template>
    <div class="task">
        <h3>{{ task.title }}</h3>
        <p>{{ task.description }}</p>

        <label>Status: {{ task.status }}</label>
        <select v-model="task.status" @change="handleMove(task.status)">
            <option value="1">To Do</option>
            <option value="2">In Progress</option>
            <option value="3">Done</option>
        </select>

        <div>
            <button class="btn btn-primary" @click="handleEdit">Edit Task</button>
            <button class="btn btn-danger" @click="handleDelete">Delete Task</button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { defineProps } from 'vue';
    import type { TaskType } from '../types/Task';

    const props = defineProps<{
        task: TaskType;
    }>();

    const emit = defineEmits<{
        (e: 'edit-task', task: TaskType): void;
        (e: 'delete-task', task: TaskType): void;
        (e: 'move-task', payload: { task: TaskType; fromColumn: number; toColumn: number }): void;
    }>();

    const handleEdit = () => {
        emit('edit-task', props.task);
    };

    const handleDelete = () => {
        emit('delete-task', props.task);
    };

    const handleMove = (toColumn: number) => {
        emit('move-task', { task: props.task, fromColumn: props.task.status, toColumn });
    };

</script>
