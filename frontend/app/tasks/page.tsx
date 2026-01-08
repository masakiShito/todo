'use client'

import { useEffect, useState } from 'react'
import TaskCard from '../../components/TaskCard'
import { API_BASE } from '../../lib/api'

interface Task {
  id: number
  title: string
  priority: string
  due_date?: string | null
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [title, setTitle] = useState('')

  const loadTasks = () => {
    fetch(`${API_BASE}/api/tasks`)
      .then(res => res.json())
      .then(data => setTasks(data.items))
  }

  useEffect(() => {
    loadTasks()
  }, [])

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    await fetch(`${API_BASE}/api/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    })
    setTitle('')
    loadTasks()
  }

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold text-slate-700">タスク詳細・作成</h2>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={title}
          onChange={event => setTitle(event.target.value)}
          placeholder="新しいタスク名"
          className="flex-1 rounded-full border border-base-200 bg-white px-4 py-2"
        />
        <button
          type="submit"
          className="rounded-full bg-accent-blue px-4 py-2 text-sm font-semibold text-slate-600"
          disabled={!title}
        >
          追加
        </button>
      </form>
      <div className="grid gap-4 md:grid-cols-2">
        {tasks.map(task => (
          <TaskCard key={task.id} title={task.title} priority={task.priority} dueDate={task.due_date} />
        ))}
      </div>
    </div>
  )
}
