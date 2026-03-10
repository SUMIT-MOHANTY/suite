import React, { useEffect, useState } from 'react';
import { Todo } from './todo';

export default function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTitle, setNewTitle] = useState('');

  const loadTodos = async () => {
    const res = await fetch('/api/v1/todos');
    setTodos(await res.json());
  };

  const addTodo = async () => {
    if (!newTitle.trim()) return;
    await fetch('/api/v1/todos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newTitle })
    });
    setNewTitle('');
    loadTodos();
  };

  const toggleTodo = async (id: string, done: boolean) => {
    await fetch(`/api/v1/todos/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done: !done })
    });
    loadTodos();
  };

  useEffect(() => { loadTodos(); }, []);

  return (
    <div>
      <input 
        value={newTitle} 
        onChange={e => setNewTitle(e.target.value)}
        placeholder="New todo..."
      />
      <button onClick={addTodo}>Add</button>
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>
            <label>
              <input 
                type="checkbox" 
                checked={todo.done}
                onChange={() => toggleTodo(todo.id, todo.done)}
              />
              {todo.title}
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}
