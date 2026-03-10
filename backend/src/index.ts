import express from 'express'
import health from './routes/health'
import todos from './routes/todos'

const app = express()
app.use(express.json())

app.use(health)
app.use(todos)

const port = process.env.PORT || 4000
app.listen(port, () => console.log(`🚀 API listening at ${port}`))
