interface StatCardProps {
  title: string
  value: number
  tone: string
}

export default function StatCard({ title, value, tone }: StatCardProps) {
  return (
    <div className={`rounded-xl border border-base-200 bg-white p-4 shadow-soft ${tone}`}>
      <p className="text-sm text-slate-500">{title}</p>
      <p className="mt-2 text-2xl font-semibold text-slate-700">{value}</p>
    </div>
  )
}
