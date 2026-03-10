import { Router } from 'express';
import db from '../clients/db';

export const router = Router();

router.get('/', async (_req, res) => {
  const uptime = process.uptime();
  let connected = false;

  try {
    // Basic ping test
    await db.raw('SELECT 1');
    connected = true;
  } catch (e) {
    console.error('DB health check failed', e);
  }

  res.json({
    status: 'ok',
    uptime,
    db: {
      connected
    }
  });
});
