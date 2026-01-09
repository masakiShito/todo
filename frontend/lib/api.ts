export const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000'

export async function fetcher<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
    ...options
  })
  if (!response.ok) {
    const text = await response.text()
    throw new Error(text)
  }
  return response.json() as Promise<T>
}
