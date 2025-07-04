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
import api from '../api/api'

const columns = ref<ColumnType[]>([])

const colorMap = {
  1: 'column-blue',
  2: 'column-yellow',
  3: 'column-red',
}

onMounted(async () => {
  try {
    const response = await api.get('/kanban_board')
    columns.value = response.data
    // Give each column a color based on its ID
    columns.value.forEach((column) => {
      column.colorClass = colorMap[column.id as keyof typeof colorMap]
    })
  } catch (error) {
    console.error('Error fetching tasks:', error)
  }
})

async function editTask(payload: {
  taskId: number
  newTitle: string
  newDescription: string
  status: number
}) {
  try {
    const response = await api.put(`/kanban_board/${payload.taskId}`, {
      title: payload.newTitle,
      description: payload.newDescription,
      status: Number(payload.status),
    })
    const updatedTask = response.data
    const column = columns.value.find((c) => c.id === Number(payload.status))
    if (column) {
      const task = column.tasks.find((t) => t.id === payload.taskId)
      if (task) {
        task.title = updatedTask.title
        task.description = updatedTask.description
        console.log('Updated task:', task)
      } else {
        console.error('Task not found in column:', payload.taskId)
      }
    } else {
      console.error('Column not found for task status:', Number(payload.status))
    }
  } catch (error) {
    console.error('Error updating task:', error)
  }
}

async function deleteTask(taskId: number) {
  try {
    await api.delete(`/kanban_board/${taskId}`)
    // Find the column that contains the task
    const column = columns.value.find((c) => c.tasks.some((t) => t.id === taskId))
    if (column) {
      // Remove the task from the column
      column.tasks = column.tasks.filter((t) => t.id !== taskId)
      console.log('Deleted task with ID:', taskId)
    }
  } catch (error) {
    console.error('Error deleting task:', error)
  }
}

async function moveTask(payload: { task: TaskType; fromColumn: number; toColumn: number }) {
  try {
    const { task, fromColumn } = payload
    const toColumn = Number(payload.toColumn)
    if (fromColumn === toColumn) {
      return
    }

    await api.put(`/kanban_board/${task.id}`, {
      title: task.title,
      description: task.description,
      status: toColumn,
    })

    const sourceColumn = columns.value.find((c) => c.id === fromColumn)
    const targetColumn = columns.value.find((c) => c.id === toColumn)

    //remove task from source column
    if (sourceColumn) {
      sourceColumn.tasks = sourceColumn.tasks.filter((t) => t.id !== task.id)
    }

    // Update task status
    task.status = toColumn

    // Add task to the target column
    if (targetColumn) {
      targetColumn.tasks.push(task)
    }

    console.log('Moved task:', task.id, 'from column', fromColumn, 'to column', toColumn)
  } catch (error) {
    console.error('Error moving task:', error)
  }
}

async function addTask(task: TaskType) {
  try {
    const response = await api.post('/kanban_board', task)
    const newTask = response.data
    // Find the column to which the task should be added
    const column = columns.value.find((c) => c.id === Number(task.status))
    if (column) {
      column.tasks.push(newTask)
      console.log('Added task:', newTask, 'to column ID:', Number(task.status))
    } else {
      console.error('Column not found for task status:', Number(task.status))
    }
  } catch (error) {
    console.error('Error adding task:', error)
  }
}

async function handleDragTask(payload: { task: TaskType; fromColumn: number; toColumn: number }) {
  try {
    const { task, fromColumn, toColumn } = payload

    if (fromColumn === toColumn) {
      return
    }

    await api.put(`/kanban_board/${task.id}`, {
      title: task.title,
      description: task.description,
      status: toColumn,
    })

    task.status = toColumn

    console.log('Dragged task:', task.id, 'from column', fromColumn, 'to column', toColumn)
  } catch (error) {
    console.error('Error updating task via drag:', error)
  }
}
</script>
