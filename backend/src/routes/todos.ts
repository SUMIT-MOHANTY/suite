import { Router } from 'express';
import { createTodo, getTodos, updateTodo, deleteTodo } from '../db/inMemoryRepo';
import { Todo } from '../todo';

export const todosRouter = Router();

todosRouter.get('/', (req, res) => {
  res.json(getTodos());
});

todosRouter.post('/', (req, res) => {
  const { title } = req.body;
  if (!title?.trim()) return res.status(400).json({ error: 'Title required' });
  
  const todo = createTodo(title.trim());
  res.status(201).json(todo);
});

todosRouter.patch('/:id', (req, res) => {
  const { done } = req.body;
  if (typeof done !== 'boolean') return res.status(400).json({ error: 'Done required' });
  
  const todo = updateTodo(req.params.id, done);
  if (!todo) return res.status(404).json({ error: 'Todo not found' });
  
  res.json(todo);
});

todosRouter.delete('/:id', (req, res) => {
  const deleted = deleteTodo(req.params.id);
  if (!deleted) return res.status(404).json({ error: 'Todo not found' });
  res.status(204).send();
});
