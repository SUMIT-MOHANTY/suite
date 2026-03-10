import React, { useEffect, useState } from 'react'

interface Todo {
  id: string
  title: string
  done: boolean
}

const App: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([])
  const [title, setTitle] = useState('')

  useEffect(() => {
    fetch('/api/v1/todos').then(r => r.json()).then(setTodos)
  }, [])

  const addTodo = async () => {
    if (!title.trim()) return
    const res = await fetch('/api/v1/todos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    })
    const todo = await res.json()
    setTodos([...todos, todo])
    setTitle('')
  }

  const toggleTodo = async (id: string, done: boolean) => {
    const res = await fetch(`/api/v1/todos/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done: !done })
    })
    const updated = await res.json()
    setTodos(todos.map(t => t.id === id ? updated : t))
  }

  const delTodo = async (id: string) => {
    await fetch(`/api/v1/todos/${id}`, { method: 'DELETE' })
    setTodos(todos.filter(t => t.id !== id))
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Todos</h1>
      <input value={title} onChange={e => setTitle(e.target.value)} />
      <button onClick={addTodo}>Add</button>
      <ul>
        {todos.map(t =>
          <li key={t.id}>
            <input type="checkbox" checked={t.done} onChange={() => toggleTodo(t.id, t.done)} />
            {t.title}
            <button onClick={() => delTodo(t.id)}>x</button>
          </li>
        )}
      </ul>
    </div>
  )
}

export default App
