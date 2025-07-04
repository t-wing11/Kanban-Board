import axios from 'axios'
import type { TaskType } from '../types/Task'

const api = axios.create({
  baseURL: 'http://localhost:5000/',
  withCredentials: true
})

export const getTasks = () => api.get('kanban_board')
export const createTask = (task: TaskType) =>
  api.post('kanban_board', task)
export const updateTask = (task: TaskType) =>
  api.put(`kanban_board/${task.id}`, task)
export const removeTask = (taskId: number) =>
  api.delete(`kanban_board/${taskId}`)
export const login = (username: string, password: string) =>
  api.post(`kanban_board/login`, { username, password })
