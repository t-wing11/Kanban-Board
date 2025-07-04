<template>
  <div :class="['task', `variant--${props.colorClass}`]">
    <div class="task-header">{{ task.title }}</div>
    <div class="task-description">{{ task.description }}</div>

    <div class="status-select-container">
      <label for="status-select">Status:</label>
      <select v-model="task.status" @change="handleMove(task.status)">
        <option value="1">To Do</option>
        <option value="2">In Progress</option>
        <option value="3">Done</option>
      </select>
    </div>

    <div class="task-footer">
      <template v-if="!taskFormVisible">
        <button class="task-footer-button" @click="taskFormVisible = true">Edit Task</button>
        <button class="task-footer-button" @click="handleDelete">Delete Task</button>
      </template>
      <CreateTask
        v-if="taskFormVisible"
        :task="task"
        :isEdit="true"
        :colorClass="props.colorClass"
        @edit-task="handleEdit"
        @cancel="taskFormVisible = false"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, defineEmits } from 'vue'
import type { TaskType } from '../types/Task'
import CreateTask from './CreateTask.vue'

const props = defineProps<{
  task: TaskType
  colorClass?: string
}>()

const emit = defineEmits<{
  (
    e: 'edit-task',
    payload: { taskId: number; newTitle: string; newDescription: string; status: number },
  ): void
  (e: 'delete-task', task: TaskType): void
  (e: 'move-task', payload: { task: TaskType; fromColumn: number; toColumn: number }): void
}>()

const handleEdit = (payload: {
  taskId: number
  newTitle: string
  newDescription: string
  status: number
}) => {
  emit('edit-task', {
    taskId: payload.taskId,
    newTitle: payload.newTitle,
    newDescription: payload.newDescription,
    status: payload.status,
  })
  taskFormVisible.value = false
}

const handleDelete = () => {
  emit('delete-task', props.task)
}

const handleMove = (toColumn: number) => {
  emit('move-task', { task: props.task, fromColumn: props.task.status, toColumn })
}

const taskFormVisible = ref(false)
</script>
