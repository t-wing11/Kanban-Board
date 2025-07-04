export interface TaskType {
  id: number
  title: string
  description: string
  status: number
  due_date: string | null
  tags: string[]
}
