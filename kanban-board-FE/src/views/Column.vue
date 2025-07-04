<template>
  <div :class="['column', `variant--${column.colorClass}`]">
    <div class="column-header">{{ column.title }}</div>

    <draggable
      class="column-tasks"
      v-model="column.tasks"
      item-key="id"
      group="tasks"
      :data-column-id="column.id"
      @change="onDrag"
      >
      <template #item="{ element: task }">
      <Task
        :key="task.id"
        :task="task"
        :colorClass="column.colorClass"
        @edit-task="editTask"
        @delete-task="deleteTask"
        @move-task="moveTask"
      />
    </template>
    </draggable>
    <div class="column-footer">
      <button class="add-Button" v-if="!taskFormVisible" @click="taskFormVisible = true">
        Add Task <span class="button-icon">➕</span>
      </button>
      <CreateTask
        v-if="taskFormVisible"
        :task="{ id: 0, title: '', description: '', status: column.id }"
        :isEdit="false"
        :colorClass="column.colorClass"
        @save-task="addTask"
        @edit-task="editTask"
        @cancel="taskFormVisible = false"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref } from 'vue'
import { ColumnType } from '../types/Column'
import type { TaskType } from '../types/Task'
import Task from './Task.vue'
import CreateTask from './CreateTask.vue'
import draggable from 'vuedraggable'

const props = defineProps<{
  column: ColumnType
}>()

const emit = defineEmits<{
  (
    e: 'edit-task',
    payload: { taskId: number; newTitle: string; newDescription: string; status: number },
  ): void
  (e: 'delete-task', taskId: number): void
  (e: 'move-task', payload: { task: TaskType; fromColumn: number; toColumn: number }): void
  (e: 'add-task', task: TaskType): void
  (e: 'drag-task', payload: { task: TaskType; fromColumn: number; toColumn: number }): void
}>()

const taskFormVisible = ref(false)

function editTask(payload: {
  taskId: number
  newTitle: string
  newDescription: string
  status: number
}) {
  emit('edit-task', {
    taskId: payload.taskId,
    newTitle: payload.newTitle,
    newDescription: payload.newDescription,
    status: payload.status,
  })
}

function deleteTask(task: TaskType) {
  emit('delete-task', task.id)
}

function moveTask(payload: { task: TaskType; fromColumn: number; toColumn: number }) {
  const fromColumn = props.column.id
  const toColumn = payload.toColumn
  const task = payload.task
  emit('move-task', { task, fromColumn, toColumn })
}

function onDrag(event: any) {
  // Handle when a task is added to this column (dragged from another column)
  if (event.added) {
    const task = event.added.element
    const fromColumnId = task.status // Original column ID from task status
    const toColumnId = props.column.id

    emit('drag-task', {
      task: task,
      fromColumn: fromColumnId,
      toColumn: toColumnId,
    })
  }
}

function addTask(task: TaskType) {
  const newTask = {
    ...task,
    id: Date.now(),
  }
  emit('add-task', newTask)
  taskFormVisible.value = false
}
</script>
