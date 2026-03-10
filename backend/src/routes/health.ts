import { Router } from 'express';
import db from "../db";

export const healthRouter = Router();

healthRouter.get('/', async (_req, res) => {
  try {
    await db.query('SELECT 1');
    res.json({ status: 'ok', uptime: process.uptime(), db: { connected: true } });
  } catch {
    res.status(500).json({ status: 'error', uptime: process.uptime(), db: { connected: false } });
  }
});
