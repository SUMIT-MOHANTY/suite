import Database from 'better-sqlite3';
import { mkdirSync } from 'fs';
import path from 'path';

const dbPath = process.env.FALLBACK_DB_PATH || '/workspace/backend/var/app.db';
mkdirSync(path.dirname(dbPath), { recursive: true });

export const db = new Database(dbPath);
