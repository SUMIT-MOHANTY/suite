import { Router } from 'express';
import { v4 as uuid } from 'uuid';
import db from '../clients/db';

export const router = Router();

interface Todo {
  id: string;
  title: string;
  done: boolean;
}

router.get('/', async (_req, res) => {
  const rows = await db('todos').select();
  const todos: Todo[] = rows.map((row: any) => ({
    id: row.id,
    title: row.title,
    done: Boolean(row.done),
  }));
  res.json(todos);
});

router.post('/', async (req, res) => {
  const { title } = req.body;
  if (!title || typeof title !== 'string' || !title.trim()) {
    return res.status(400).json({ error: 'Title is required' });
  }
  const todo: Todo = { id: uuid(), title: title.trim(), done: false };
  await db('todos').insert(todo);
  res.status(201).json(todo);
});

router.patch('/:id', async (req, res) => {
  const { id } = req.params;
  const { title, done } = req.body;
  const updates: any = {};

  if (title !== undefined) updates.title = title.trim?.() ?? title;
  if (done !== undefined) updates.done = Boolean(done);

  if (Object.keys(updates).length === 0) {
    return res.status(400).json({ error: 'No valid fields to update' });
  }

  const [updated] = await db('todos').where({ id }).update(updates).returning('*');
  if (!updated) {
    return res.status(404).json({ error: 'Todo not found' });
  }

  res.json(updated);
});

router.delete('/:id', async (req, res) => {
  const { id } = req.params;
  await db('todos').where({ id }).del();
  res.status(204).end();
});
