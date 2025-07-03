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
      <button class="btn btn-primary" @click="taskFormVisible = true">Edit Task</button>
      <TaskForm
        v-if="taskFormVisible"
        :task="task"
        :isEdit="true"
        @edit-task="handleEdit"
        @cancel="taskFormVisible = false"
      />
      <button class="btn btn-danger" @click="handleDelete">Delete Task</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, defineEmits } from 'vue'
import type { TaskType } from '../types/Task'
import TaskForm from './CreateTask.vue'

const props = defineProps<{
  task: TaskType
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
