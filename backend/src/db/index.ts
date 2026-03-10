import sqlite3 from 'sqlite3'
import { resolve } from 'path'

const init = () => {
  if (process.env.NODE_ENV === 'test') return { query: () => [] }
  const dir = resolve(__dirname, '../../data')
  const db = new sqlite3.Database(resolve(dir, 'dev.db'))
  db.exec(`
    CREATE TABLE IF NOT EXISTS todos(
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      done BOOLEAN NOT NULL CHECK(done IN (0,1)),
      created TEXT NOT NULL,
      updated TEXT NOT NULL
    )
  `)
  return {
    query: (sql: string, params: any[] = []) =>
      new Promise<any[]>((resolve, reject) =>
        db.all(sql, params, (err, rows) => (err ? reject(err) : resolve(rows)))
      )
  }
}

export default init()
