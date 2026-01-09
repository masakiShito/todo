'use client'

import { useEffect, useMemo, useState } from 'react'
import { addDays, format } from 'date-fns'
import TaskCard from '../../components/TaskCard'
import { API_BASE } from '../../lib/api'

interface Task {
  id: number
  title: string
  priority: string
  due_date: string | null
}

export default function TimelinePage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [status, setStatus] = useState('')
  const [priority, setPriority] = useState('')

  const start = new Date()
  const end = addDays(start, 14)

  const query = useMemo(() => {
    const params = new URLSearchParams({
      start: format(start, 'yyyy-MM-dd'),
      end: format(end, 'yyyy-MM-dd')
    })
    if (status) params.append('status', status)
    if (priority) params.append('priority', priority)
    return params.toString()
  }, [start, end, status, priority])

  useEffect(() => {
    fetch(`${API_BASE}/api/timeline?${query}`)
      .then(res => res.json())
      .then(data => setTasks(data))
  }, [query])

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <h2 className="text-lg font-semibold text-slate-700">タイムライン</h2>
        <div className="flex gap-2 text-sm">
          <select
            value={status}
            onChange={event => setStatus(event.target.value)}
            className="rounded-full border border-base-200 bg-white px-3 py-2"
          >
            <option value="">全ステータス</option>
            <option value="backlog">Backlog</option>
            <option value="in_progress">In Progress</option>
            <option value="review">Review</option>
            <option value="done">Done</option>
          </select>
          <select
            value={priority}
            onChange={event => setPriority(event.target.value)}
            className="rounded-full border border-base-200 bg-white px-3 py-2"
          >
            <option value="">全優先度</option>
            <option value="P0">P0</option>
            <option value="P1">P1</option>
            <option value="P2">P2</option>
            <option value="P3">P3</option>
          </select>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {tasks.map(task => (
          <TaskCard key={task.id} title={task.title} priority={task.priority} dueDate={task.due_date} />
        ))}
      </div>
      {tasks.length === 0 && <p className="text-sm text-slate-500">対象期間のタスクがありません。</p>}
    </div>
  )
}
