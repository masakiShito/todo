import { ReactNode } from 'react'

interface KanbanColumnProps {
  title: string
  count: number
  children: ReactNode
}

export default function KanbanColumn({ title, count, children }: KanbanColumnProps) {
  return (
    <div className="flex min-w-[240px] flex-1 flex-col gap-3 rounded-xl border border-base-200 bg-base-50 p-4">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold text-slate-600">{title}</h2>
        <span className="rounded-full bg-white px-2 py-1 text-xs text-slate-500">{count}</span>
      </div>
      <div className="flex flex-1 flex-col gap-3">{children}</div>
    </div>
  )
}
