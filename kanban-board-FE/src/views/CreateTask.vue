<template>
  <div class="modal-overlay" @click.self="cancel">
    <div :class="['modal-content', `variant--${props.colorClass}`]">
      <div class="form-container">
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="title">Title</label>
            <input type="text" id="title" v-model="task.title" class="form-control" required />
          </div>
          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="task.description"
              class="form-control"
              required
            ></textarea>
          </div>
          <div class="status-select-container" v-if="!props.isEdit">
            <label>Status:</label>
            <select v-model="task.status">
              <option value="1">To Do</option>
              <option value="2">In Progress</option>
              <option value="3">Done</option>
            </select>
          </div>
          <div class="dueDate">
            <label for="due_date">Due Date:</label>
            <input
              id="due_date"
              type="date"
              v-model="task.due_date"
              class="input"
            />
          </div>
          <div class="tag-select-container">
            <label for="tags">Tags:</label>
            <select id="tags" v-model="task.tags" multiple>
              <option value="urgent">Urgent</option>
              <option value="important">Important</option>
              <option value="optional">Optional</option>
            </select>
          </div>
          <div class="form-footer">
            <button type="submit">Save Task</button>
            <button type="button" @click="cancel">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineEmits, defineProps, ref } from 'vue'
import type { TaskType } from '../types/Task'

const props = defineProps<{
  task?: TaskType | null
  isEdit: boolean
  colorClass?: string
}>()

// If task is provided, use its values; otherwise, initialize with default values
const task = ref<TaskType>({
  id: props.task?.id || 0,
  title: props.task?.title || '',
  description: props.task?.description || '',
  status: props.task!.status,
  due_date: props.task?.due_date || null,
  tags: props.task?.tags || [],
})

// Define the emits for the component
const emit = defineEmits<{
  (e: 'save-task', task: TaskType): void
  (
    e: 'edit-task',
    payload: { taskId: number; newTitle: string; newDescription: string; status: number; dueDate: string | null; tags: string[] },
  ): void
  (e: 'cancel'): void
}>()

// Function Definitions

function handleSubmit() {
  if (props.isEdit) {
    emit('edit-task', {
      taskId: task.value.id,
      newTitle: task.value.title,
      newDescription: task.value.description,
      status: task.value.status,
      dueDate: task.value.due_date,
      tags: task.value.tags,
    })
  } else {
    emit('save-task', task.value)
  }
}

function cancel() {
  emit('cancel')
}
</script>
