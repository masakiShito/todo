import StatCard from '../components/StatCard'
import TaskCard from '../components/TaskCard'
import { API_BASE } from '../lib/api'

interface DashboardSummary {
  overdue: number
  today: number
  this_week: number
  no_due: number
}

interface Task {
  id: number
  title: string
  priority: string
  due_date?: string | null
  category_id?: number | null
  parent_task_id?: number | null
}

async function getSummary(): Promise<DashboardSummary> {
  const res = await fetch(`${API_BASE}/api/dashboard/summary`, { cache: 'no-store' })
  return res.json()
}

async function getUrgent(): Promise<{ items: Task[] }> {
  const res = await fetch(`${API_BASE}/api/dashboard/urgent`, { cache: 'no-store' })
  return res.json()
}

export default async function DashboardPage() {
  const [summary, urgent] = await Promise.all([getSummary(), getUrgent()])

  return (
    <div className="space-y-8">
      <section className="grid gap-4 md:grid-cols-4">
        <StatCard title="期限超過" value={summary.overdue} tone="" />
        <StatCard title="今日" value={summary.today} tone="" />
        <StatCard title="今週" value={summary.this_week} tone="" />
        <StatCard title="未設定" value={summary.no_due} tone="" />
      </section>

      <section className="rounded-xl border border-base-200 bg-white p-6 shadow-soft">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-700">期限が近いタスク</h2>
          <span className="text-xs text-slate-500">7日以内の未完了</span>
        </div>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          {urgent.items.map(task => (
            <TaskCard
              key={task.id}
              title={task.title}
              priority={task.priority}
              dueDate={task.due_date}
              childCount={0}
            />
          ))}
          {urgent.items.length === 0 && <p className="text-sm text-slate-500">該当するタスクはありません。</p>}
        </div>
      </section>
    </div>
  )
}
