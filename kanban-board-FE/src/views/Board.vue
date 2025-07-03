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
  import { ref } from 'vue';
  import { ColumnType } from '../types/Column';
  import type { TaskType } from '../types/Task';
  import Column from './Column.vue';

  const columns = ref<ColumnType[]>([
    {
      id: 1,
      title: 'To Do',
      tasks: []
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

  function editTask(payload: { taskId: number; newTitle: string; newDescription: string }) {
    // Find the column that contains the task
    const column = columns.value.find(c => c.tasks.some(t => t.id === payload.taskId));
    // Update the tasks contents
    if (column) {
      // Update the task title and description
      const task = column.tasks.find(t => t.id === payload.taskId);
      if (task) {
        task.title = payload.newTitle;
        task.description = payload.newDescription;
        console.log('Updated task:', task);
      }
    }

  }

  function deleteTask(taskId: number) {
    columns.value.forEach(c => {
      c.tasks = c.tasks.filter(t => t.id !== taskId);
    });
    console.log('Deleted task with ID:', taskId);
  }

  function moveTask(payload: { task: TaskType; fromColumn: number; toColumn: number }) {
      const { task, fromColumn } = payload;
      const toColumn = Number(payload.toColumn);

      if (fromColumn === toColumn) {
          return;
      }

      // Remove task from the source column
      const sourceColumn = columns.value.find(c => c.id === fromColumn);
      const targetColumn = columns.value.find(c => c.id === toColumn);

      //remove task from source column
      if (sourceColumn) {
          sourceColumn.tasks = sourceColumn.tasks.filter(t => t.id !== task.id);
      }

      // Update task status
      task.status = toColumn;

      // Add task to the target column
      if (targetColumn) {
          targetColumn.tasks.push(task);
      }
  }

  function addTask(task: TaskType) {
      const column = columns.value.find(c => c.id === Number(task.status));
      if (column) {
          column.tasks.push(task);
      }
      console.log('Added task:', task, 'to column ID:', task.status);
  }

</script>
