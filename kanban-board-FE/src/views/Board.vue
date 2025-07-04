<template>
  <div class="board">
    <Column
      v-for="column in columns"
      :key="column.id"
      :column="column"
      @edit-task="editTask"
      @delete-task="deleteTask"
      @move-task="moveTask"
      @add-task="addTask"
      @drag-task="handleDragTask"
    />
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { ColumnType } from '../types/Column'
  import type { TaskType } from '../types/Task'
  import Column from './Column.vue'
  import { getTasks, createTask, updateTask, removeTask } from '../api/api'

  const columns = ref<ColumnType[]>([])

  const colorMap = {
    1: 'column-blue',
    2: 'column-yellow',
    3: 'column-red',
  }

  // Load the board
  onMounted(async () => {
    try {
      const response = await getTasks()
      columns.value = response.data
      // Give each column a color based on its ID
      columns.value.forEach((column) => {
        column.colorClass = colorMap[column.id as keyof typeof colorMap]
      })
    } catch (error) {
      console.error('Error fetching tasks:', error)
    }
  })

  // Edit task backend call
  async function editTask(payload: {
    taskId: number
    newTitle: string
    newDescription: string
    status: number
    dueDate?: string | null
    tags?: string[]
  }) {
    try {
      const response = await updateTask({
        id: payload.taskId,
        title: payload.newTitle,
        description: payload.newDescription,
        status: Number(payload.status),
        due_date: payload.dueDate ?? null,
        tags: payload.tags ?? [],
      })

      const updatedTask = response.data
      const column = columns.value.find((c) => c.id === Number(payload.status))

      if (column) {
        const task = column.tasks.find((t) => t.id === payload.taskId)
        if (task) {
          task.title = updatedTask.title
          task.description = updatedTask.description
          task.status = updatedTask.status
          task.due_date = updatedTask.due_date
          task.tags = updatedTask.tags
        } 
      } 
    } catch (error) {
      console.error('Error updating task:', error)
    }
  }

  // Delete task backend call
  async function deleteTask(taskId: number) {
    try {
      await removeTask(taskId)

      const column = columns.value.find((c) => c.tasks.some((t) => t.id === taskId))
      if (column) {
        column.tasks = column.tasks.filter((t) => t.id !== taskId)
      }
    } catch (error) {
      console.error('Error deleting task:', error)
    }
  }

  // Move task backend call
  async function moveTask(payload: { task: TaskType; fromColumn: number; toColumn: number }) {
    try {
      const { task, fromColumn } = payload
      const toColumn = Number(payload.toColumn)
      
      if (fromColumn === toColumn) {
        return
      }

      await updateTask({
        id: task.id,
        title: task.title,
        description: task.description,
        status: toColumn,
        due_date: task.due_date,
        tags: task.tags,
      })

      const sourceColumn = columns.value.find((c) => c.id === fromColumn)
      const targetColumn = columns.value.find((c) => c.id === toColumn)

      if (sourceColumn) {
        sourceColumn.tasks = sourceColumn.tasks.filter((t) => t.id !== task.id)
      }

      task.status = toColumn

      if (targetColumn) {
        targetColumn.tasks.push(task)
      }
    } catch (error) {
      console.error('Error moving task:', error)
    }
  }

  // Add task backend call
  async function addTask(task: TaskType) {
    try {
      const response = await createTask(task)
      const newTask = response.data

      const column = columns.value.find((c) => c.id === Number(task.status))

      if (column) {
        column.tasks.push(newTask)
      } 
    } catch (error) {
      console.error('Error adding task:', error)
    }
  }

  // Handle drag task event
  async function handleDragTask(payload: { task: TaskType; fromColumn: number; toColumn: number }) {
    try {
      const { task, fromColumn, toColumn } = payload

      if (fromColumn === toColumn) {
        return
      }

      await updateTask({
        id: task.id,
        title: task.title,
        description: task.description,
        status: toColumn,
        due_date: task.due_date,
        tags: task.tags,
      })

      task.status = toColumn
    } catch (error) {
      console.error('Error updating task via drag:', error)
    }
  }
</script>
