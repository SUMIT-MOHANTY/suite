import knex from 'knex';

const config = {
  client: process.env.NODE_ENV === 'development' ? 'sqlite3' : 'pg',
  connection: process.env.DATABASE_URL || 'file:///workspace/backend/data/dev.db',
  useNullAsDefault: true
};

export default knex(config);
