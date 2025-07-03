import axios from 'axios'
import type { TaskType } from '../types/Task'
import { h } from 'vue'

const api = axios.create({
  baseURL: 'http://localhost:5000/',
})

// export const getTasks = () => axios.get(API_BASE);
// export const createTask = (task: TaskType) => axios.post(API_BASE, task);
// export const updateTask = (task: TaskType) => axios.put(`${API_BASE}/${task.id}`, task);
// export const removeTask = (taskId: string) => axios.delete(`${API_BASE}/${taskId}`);

export default api
