<template>
    <div class="column">
        <h2>{{ column.title }}</h2>

        <div class="tasks">
            <Task v-for="task in column.tasks" :key="task.id" :task="task" @edit-task="editTask" @delete-task="deleteTask" @move-task="moveTask" />
        </div>
        <button class="btn btn-primary" @click="taskFormVisible = true">Add Task</button>
        <TaskForm v-if="taskFormVisible" @save-task="handleSaveTask" @cancel="taskFormVisible = false" />
    </div>

</template>

<script setup lang="ts">
    import Task from './Task.vue';
    import { defineProps, defineEmits } from 'vue';
    import { ColumnType } from '../types/Column';
    import type { TaskType } from '../types/Task';
    import TaskForm from './CreateTask.vue';
    import { ref } from 'vue';

    const props = defineProps<{
        column: ColumnType;
    }>();

    const emit = defineEmits<{
        (e: 'edit-task', task: TaskType): void;
        (e: 'delete-task', taskId: number): void;
        (e: 'move-task', payload: { task: TaskType; fromColumn: number; toColumn: number }): void;
        (e: 'add-task', payload: { columnId: number, task: TaskType }): void;
    }>();

    const taskFormVisible = ref(false);

    function editTask(task: TaskType) {
        emit('edit-task', task)
    }

    function deleteTask(task: TaskType) {
        emit('delete-task', task.id)
    }

    function moveTask(payload: { task: TaskType; fromColumn: number; toColumn: number }) {
        const fromColumn = props.column.id; 
        const toColumn = payload.toColumn;
        const task = payload.task;
        emit('move-task', { task, fromColumn, toColumn });
    }
    
    function handleSaveTask(newTask: TaskType) {
        emit('add-task', { columnId: props.column.id, task: newTask })
        taskFormVisible.value = false
    }
</script>
