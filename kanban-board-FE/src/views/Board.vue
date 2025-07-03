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
        />
        
    </div>
</template>

<script setup lang="ts">
import Column from './Column.vue';
import { ref } from 'vue';
import { ColumnType } from '../types/Column';
import type { TaskType } from '../types/Task';

const columns = ref<ColumnType[]>([
  {
    id: 1,
    title: 'To Do',
    tasks: [
      {
        id: 1,
        title: 'Task 1',
        description: 'Description for Task 1',
        status: 1
      },
      {
        id: 2,
        title: 'Task 2',
        description: 'Description for Task 2',
        status: 1
      }
    ]
  },
  {
    id: 2,
    title: 'In Progress',
    tasks: []
  },
  {
    id: 3,
    title: 'Done',
    tasks: []
  }
]);

function editTask(task: TaskType) {
  // Implement edit task logic here

} 

function deleteTask(taskId: number) {
  columns.value.forEach(c => {
    c.tasks = c.tasks.filter(t => t.id !== taskId);
  });
}

function moveTask(payload: { task: TaskType; fromColumn: number; toColumn: number }) {
  
}

function addTask() {
    // Implement add task logic here

}
</script>
