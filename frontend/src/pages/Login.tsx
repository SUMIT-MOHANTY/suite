import { useState } from 'react';
import { authStore } from '../store/auth';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const login = () => { authStore.setToken('mock'); window.location.href = '/'; };
  
  return (
    <div>
      <h1>Login</h1>
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="email" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="password" />
      <button onClick={login}>Login</button>
    </div>
  );
}
