import { Router } from 'express'
import { v4 as uuid } from 'uuid'
import db from "../db"

const router = Router()

router.get('/api/v1/todos', async (_req, res) => {
  const rows = await db.query('SELECT id,title,done FROM todos')
  res.json(rows)
})

router.post('/api/v1/todos', async (req, res) => {
  const title = (req.body.title || '').trim()
  if (!title) return res.status(400).end()
  const id = uuid()
  const created = new Date().toISOString()
  await db.query('INSERT INTO todos(id,title,done,created,updated) VALUES (?,?,false,?,?)', [id, title, created, created])
  res.status(201).json({ id, title, done: false })
})

router.patch('/api/v1/todos/:id', async (req, res) => {
  const { id } = req.params
  const { title, done } = req.body
  let sql = 'UPDATE todos SET updated = ?'
  const vals = [new Date().toISOString()]
  if (title !== undefined) { sql += ', title = ?'; vals.push(title) }
  if (done !== undefined) { sql += ', done = ?'; vals.push(done) }
  sql += ' WHERE id = ?'
  vals.push(id)
  await db.query(sql, vals)
  const [row] = await db.query('SELECT id,title,done FROM todos WHERE id = ?', [id])
  res.json(row)
})

router.delete('/api/v1/todos/:id', async (req, res) => {
  const { id } = req.params
  await db.query('DELETE FROM todos WHERE id = ?', [id])
  res.status(204).end()
})

export default router
