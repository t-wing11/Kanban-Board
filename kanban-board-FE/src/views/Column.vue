<template>
    <div class="column">
        <h2>{{ column.title }}</h2>

        <div class="tasks">
            <Task v-for="task in column.tasks" :key="task.id" :task="task" @edit-task="editTask" @delete-task="deleteTask" @move-task="moveTask" />
        </div>
        <button class="btn btn-success" @click="taskFormVisible = true">Add Task</button>
        <TaskForm v-if="taskFormVisible" 
            :task="{ id: 0, title: '', description: '', status: column.id }"
            :isEdit="false"
            @save-task="addTask" 
            @edit-task="editTask"
            @cancel="taskFormVisible = false"
        />
    </div>
</template>

<script setup lang="ts">
    import { defineProps, defineEmits, ref } from 'vue';
    import { ColumnType } from '../types/Column';
    import type { TaskType } from '../types/Task';
    import Task from './Task.vue';
    import TaskForm from './CreateTask.vue';

    const props = defineProps<{
        column: ColumnType;
    }>();

    const emit = defineEmits<{
        (e: 'edit-task', payload: { taskId: number, newTitle: string, newDescription: string, status: number }): void;
        (e: 'delete-task', taskId: number): void;
        (e: 'move-task', payload: { task: TaskType; fromColumn: number; toColumn: number }): void;
        (e: 'add-task', task: TaskType ): void;
    }>();

    const taskFormVisible = ref(false);

    function editTask(payload: { taskId: number; newTitle: string; newDescription: string, status: number }) {
        emit('edit-task', {
            taskId: payload.taskId,
            newTitle: payload.newTitle,
            newDescription: payload.newDescription,
            status: payload.status
        });
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

    function addTask(task: TaskType) {
        const newTask = {
            ...task,
            id: Date.now(),
        };
        emit('add-task', newTask);
        taskFormVisible.value = false;
    }
</script>
