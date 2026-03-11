import { Todo } from '../todo';

let todos: Todo[] = [];

export const createTodo = (title: string): Todo => {
  const todo = { id: crypto.randomUUID(), title, done: false };
  todos.push(todo);
  return todo;
};

export const getTodos = (): Todo[] => todos;

export const updateTodo = (id: string, done: boolean): Todo | null => {
  const todo = todos.find(t => t.id === id);
  if (!todo) return null;
  todo.done = done;
  return todo;
};

export const deleteTodo = (id: string): boolean => {
  const index = todos.findIndex(t => t.id === id);
  if (index === -1) return false;
  todos.splice(index, 1);
  return true;
};
