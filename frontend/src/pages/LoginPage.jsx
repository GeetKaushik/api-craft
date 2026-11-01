import { Braces, LockKeyhole } from "lucide-react"
import AuthForm from "../features/auth/AuthForm.jsx"

function LoginPage() {
  return (
    <main className="auth-page">
      <section className="auth-card" aria-labelledby="auth-title">
        <a className="brand auth-brand" href="#overview" aria-label="API Craft dashboard">
          <span className="brand-mark"><Braces size={19} strokeWidth={2.5} /></span>
          <span className="brand-name">API<span>Craft</span></span>
        </a>
        <span className="auth-icon"><LockKeyhole size={19} /></span>
        <h1 id="auth-title">Welcome back</h1>
        <p className="auth-description">Log in to continue to API Craft.</p>
        <AuthForm mode="login" />
        <p className="auth-switch">
          Don’t have an account? <a href="#register">Create one</a>
        </p>
      </section>
    </main>
  )
}

export default LoginPage
