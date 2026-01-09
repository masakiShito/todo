import '../styles/globals.css'
import Header from '../components/Header'

export const metadata = {
  title: 'Backlog風TODO',
  description: '個人用タスク管理アプリ'
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body className="min-h-screen bg-base-100">
        <Header />
        <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
      </body>
    </html>
  )
}
