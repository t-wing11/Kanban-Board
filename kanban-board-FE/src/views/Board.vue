<template>
  <div class="board-container">
    <Login v-if="!loggedIn" :error-message="errorMessage" @login="handleLogin" /> 
    <div v-else class="board">
    <Column
      v-for="column in columns"
      :key="column.id"
      :column="column"
      @edit-task="editTask"
      @delete-task="deleteTask"
      @move-task="moveTask"
      @add-task="addTask"
      @drag-task="handleDragTask"
      @login="handleLogin"
    />
  </div>
  <button class="logout-button" @click="handleLogout" v-if="loggedIn">Logout</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ColumnType } from '../types/Column'
import Column from './Column.vue'
import Login from './Login.vue'
import { manageTasks } from '../composables/manageTasks'
import { manageBoard } from '../composables/manageBoard'

const columns = ref<ColumnType[]>([])

const { editTask, deleteTask, moveTask, addTask, handleDragTask } = manageTasks(columns)

const { loggedIn, errorMessage, loadBoard, handleLogin, handleLogout } = manageBoard(columns)
// Load the board
onMounted(() => {
  if (loggedIn.value) {
    loadBoard()
  }
})
</script>
