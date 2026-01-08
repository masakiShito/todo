import { format } from 'date-fns'

interface TaskCardProps {
  title: string
  priority: string
  category?: string
  dueDate?: string | null
  childCount?: number
}

export default function TaskCard({ title, priority, category, dueDate, childCount }: TaskCardProps) {
  return (
    <div className="rounded-xl border border-base-200 bg-white p-4 shadow-soft">
      <div className="flex items-center justify-between">
        <h3 className="font-medium text-slate-700">{title}</h3>
        <span className="rounded-full bg-accent-blue px-2 py-1 text-xs text-slate-600">{priority}</span>
      </div>
      <div className="mt-2 flex flex-wrap gap-2 text-xs text-slate-500">
        {category && <span className="rounded-full bg-accent-green px-2 py-1">{category}</span>}
        {dueDate && <span className="rounded-full bg-accent-cream px-2 py-1">期限: {format(new Date(dueDate), 'MM/dd')}</span>}
        {childCount && <span className="rounded-full bg-accent-purple px-2 py-1">子 {childCount} 件</span>}
      </div>
    </div>
  )
}
