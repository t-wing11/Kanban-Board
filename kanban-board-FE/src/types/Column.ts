import type { TaskType } from '../types/Task'

export interface ColumnType {
  id: number
  title: string
  tasks: TaskType[]
  colorClass?: string
}
