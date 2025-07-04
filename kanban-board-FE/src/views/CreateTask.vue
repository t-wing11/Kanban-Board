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

const emit = defineEmits<{
  (e: 'save-task', task: TaskType): void
  (
    e: 'edit-task',
    payload: { taskId: number; newTitle: string; newDescription: string; status: number },
  ): void
  (e: 'cancel'): void
}>()

const task = ref<TaskType>({
  id: props.task?.id || 0,
  title: props.task?.title || '',
  description: props.task?.description || '',
  status: props.task!.status,
})

function handleSubmit() {
  if (props.isEdit) {
    emit('edit-task', {
      taskId: task.value.id,
      newTitle: task.value.title,
      newDescription: task.value.description,
      status: task.value.status,
    })
  } else {
    emit('save-task', task.value)
  }
}

function cancel() {
  emit('cancel')
}
</script>
