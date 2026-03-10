import { useState } from 'react';

export default function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const register = () => { window.location.href = '/login'; };
  
  return (
    <div>
      <h1>Register</h1>
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="email" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="password" />
      <button onClick={register}>Register</button>
    </div>
  );
}
