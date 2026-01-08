'use client'

import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import TaskCard from './TaskCard'

interface SortableTaskCardProps {
  id: string
  title: string
  priority: string
  dueDate?: string | null
}

export default function SortableTaskCard({ id, title, priority, dueDate }: SortableTaskCardProps) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id })
  const style = {
    transform: CSS.Transform.toString(transform),
    transition
  }

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      <TaskCard title={title} priority={priority} dueDate={dueDate} />
    </div>
  )
}
