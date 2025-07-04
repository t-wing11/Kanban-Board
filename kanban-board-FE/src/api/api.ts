import axios from 'axios'
import type { TaskType } from '../types/Task'

const api = axios.create({
  baseURL: 'http://localhost:5000/',
})

export const getTasks = () => axios.get(api.defaults.baseURL + 'kanban_board')
export const createTask = (task: TaskType) =>
  axios.post(api.defaults.baseURL + 'kanban_board', task)
export const updateTask = (task: TaskType) =>
  axios.put(api.defaults.baseURL + `kanban_board/${task.id}`, task)
export const removeTask = (taskId: number) =>
  axios.delete(api.defaults.baseURL + `kanban_board/${taskId}`)
