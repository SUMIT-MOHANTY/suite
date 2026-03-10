import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { router as healthRouter } from './routes/health';
import { router as todosRouter } from './routes/todos';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  credentials: true
}));

app.use(express.json());

// Routes
app.use('/health', healthRouter);
app.use('/api/v1/todos', todosRouter);

// 404 handler
app.use('*', (_, res) => {
  res.status(404).json({ error: 'Not Found' });
});

export default app;
