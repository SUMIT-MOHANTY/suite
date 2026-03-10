class AuthStore {
  get token() { return localStorage.getItem('token'); }
  setToken(t: string) { localStorage.setItem('token', t); }
  clear() { localStorage.removeItem('token'); }
}
export const authStore = new AuthStore();
