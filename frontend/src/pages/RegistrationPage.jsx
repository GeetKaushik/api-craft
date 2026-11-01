import { Braces, UserRoundPlus } from "lucide-react"
import AuthForm from "../features/auth/AuthForm.jsx"

function RegistrationPage() {
  return (
    <main className="auth-page">
      <section className="auth-card" aria-labelledby="auth-title">
        <a className="brand auth-brand" href="#overview" aria-label="API Craft dashboard">
          <span className="brand-mark"><Braces size={19} strokeWidth={2.5} /></span>
          <span className="brand-name">API<span>Craft</span></span>
        </a>
        <span className="auth-icon"><UserRoundPlus size={19} /></span>
        <h1 id="auth-title">Create your account</h1>
        <p className="auth-description">Get started with API Craft.</p>
        <AuthForm mode="register" />
        <p className="auth-switch">
          Already have an account? <a href="#login">Log in</a>
        </p>
      </section>
    </main>
  )
}

export default RegistrationPage
