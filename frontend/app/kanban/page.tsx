'use client'

import { useEffect, useMemo, useState } from 'react'
import { DndContext, DragEndEvent } from '@dnd-kit/core'
import { SortableContext, verticalListSortingStrategy, arrayMove } from '@dnd-kit/sortable'
import KanbanColumn from '../../components/KanbanColumn'
import SortableTaskCard from '../../components/SortableTaskCard'
import { API_BASE } from '../../lib/api'

interface Task {
  id: number
  title: string
  status: string
  priority: string
  due_date?: string | null
}

const columns = [
  { key: 'backlog', label: 'Backlog' },
  { key: 'in_progress', label: 'In Progress' },
  { key: 'review', label: 'Review' },
  { key: 'done', label: 'Done' }
]

export default function KanbanPage() {
  const [tasks, setTasks] = useState<Task[]>([])

  useEffect(() => {
    fetch(`${API_BASE}/api/tasks`)
      .then(res => res.json())
      .then(data => setTasks(data.items))
  }, [])

  const grouped = useMemo(() => {
    return columns.reduce<Record<string, Task[]>>((acc, column) => {
      acc[column.key] = tasks.filter(task => task.status === column.key)
      return acc
    }, {})
  }, [tasks])

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    if (!over) return

    const [fromStatus, fromId] = String(active.id).split(':')
    const [toStatus, toId] = String(over.id).split(':')

    if (fromStatus === toStatus) {
      const columnTasks = grouped[fromStatus]
      const oldIndex = columnTasks.findIndex(task => task.id === Number(fromId))
      const newIndex = columnTasks.findIndex(task => task.id === Number(toId))
      if (oldIndex < 0 || newIndex < 0) return
      const updated = arrayMove(columnTasks, oldIndex, newIndex)
      setTasks(prev =>
        prev.map(task => {
          const updatedTask = updated.find(item => item.id === task.id)
          return updatedTask ? updatedTask : task
        })
      )
    } else {
      setTasks(prev =>
        prev.map(task => (task.id === Number(fromId) ? { ...task, status: toStatus } : task))
      )
      fetch(`${API_BASE}/api/tasks/${fromId}/move`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: toStatus, order_index: 0 })
      })
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold text-slate-700">カンバン</h2>
      <DndContext onDragEnd={handleDragEnd}>
        <div className="flex gap-4 overflow-x-auto pb-4">
          {columns.map(column => (
            <SortableContext
              key={column.key}
              items={grouped[column.key].map(task => `${column.key}:${task.id}`)}
              strategy={verticalListSortingStrategy}
            >
              <KanbanColumn title={column.label} count={grouped[column.key].length}>
                {grouped[column.key].map(task => (
                  <SortableTaskCard
                    key={`${column.key}:${task.id}`}
                    id={`${column.key}:${task.id}`}
                    title={task.title}
                    priority={task.priority}
                    dueDate={task.due_date}
                  />
                ))}
              </KanbanColumn>
            </SortableContext>
          ))}
        </div>
      </DndContext>
    </div>
  )
}
