import Link from 'next/link'

const links = [
  { href: '/', label: 'ダッシュボード' },
  { href: '/kanban', label: 'カンバン' },
  { href: '/timeline', label: 'タイムライン' },
  { href: '/tasks', label: 'タスク一覧' }
]

export default function Header() {
  return (
    <header className="bg-white/70 backdrop-blur border-b border-base-200">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div>
          <h1 className="text-xl font-semibold text-slate-700">Backlog風TODO</h1>
          <p className="text-sm text-slate-500">個人用タスク管理</p>
        </div>
        <nav className="flex gap-4 text-sm">
          {links.map(link => (
            <Link
              key={link.href}
              href={link.href}
              className="rounded-full px-3 py-1 text-slate-600 hover:bg-base-200"
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  )
}
