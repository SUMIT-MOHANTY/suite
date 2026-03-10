import { Router } from "express";
import { v4 as uuid } from "uuid";

const router = Router();
const todos: any[] = [];

router.get("/", (_req, res) => res.json(todos));
router.post("/", (req, res) => {
  const todo = { id: uuid(), ...req.body, done: false };
  todos.push(todo);
  res.status(201).json(todo);
});
router.patch("/:id", (req, res) => {
  const idx = todos.findIndex(t => t.id === req.params.id);
  if (idx === -1) return res.status(404).end();
  todos[idx] = { ...todos[idx], ...req.body };
  res.json(todos[idx]);
});
export { router as todosRouter };
