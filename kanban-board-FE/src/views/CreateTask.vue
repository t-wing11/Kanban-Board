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
        <div v-if="!props.isEdit">
            <label>Status:</label>
            <select v-model="task.status">
                <option value="1">To Do</option>
                <option value="2">In Progress</option>
                <option value="3">Done</option>
            </select>
        </div>
        <button type="submit" class="btn btn-primary">Save Task</button>
        <button type="button" class="btn btn-secondary" @click="cancel">Cancel</button>
    </form>
</template>

<script setup lang="ts">
    import { defineEmits, defineProps, ref } from 'vue';
    import type { TaskType } from '../types/Task';

    const props = defineProps<{
        task?: TaskType | null;
        isEdit: boolean; 
    }>();

    const emit = defineEmits<{
        (e: 'save-task', task: TaskType): void;
        (e: 'edit-task', payload: { taskId: number; newTitle: string; newDescription: string }): void;
        (e: 'cancel'): void;
    }>();

    const task = ref<TaskType>({
        id: props.task?.id || 0,
        title: props.task?.title || '',
        description: props.task?.description || '',
        status: props.task!.status
    });

    function handleSubmit() {
        if (props.isEdit) {
            emit('edit-task', {
                taskId: task.value.id,
                newTitle: task.value.title,
                newDescription: task.value.description
            });
        } else {
            emit('save-task', task.value);
        }
    }

    function cancel() {
        emit('cancel');
    }

</script>