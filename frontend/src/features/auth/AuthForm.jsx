import { useState } from "react"
import { Eye, EyeOff } from "lucide-react"
import { authService } from "../../services/authService"
import { tokenService } from "../../services/tokenService"

function AuthForm({ mode }) {
  const isRegistration = mode === "register"
  const [values, setValues] = useState({
    name: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
  })
  const [errors, setErrors] = useState({})
  const [passwordVisible, setPasswordVisible] = useState(false)
  const [confirmationVisible, setConfirmationVisible] = useState(false)
  const [notice, setNotice] = useState("")

  const updateValue = (event) => {
    const { name, value } = event.target
    setValues((current) => ({ ...current, [name]: value }))
    setErrors((current) => {
      const nextErrors = { ...current }
      delete nextErrors[name]
      return nextErrors
    })
    setNotice("")
  }

  const validate = (event) => {
    const nextErrors = {}

    if (isRegistration && values.name.trim().length < 2) {
      nextErrors.name = "Enter a name with at least 2 characters."
    } else if (isRegistration && values.name.length > 100) {
      nextErrors.name = "Name must be 100 characters or fewer."
    }

    if (
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email) ||
      values.email.length > 150
    ) {
      nextErrors.email = "Enter a valid email address (up to 150 characters)."
    }

    if (isRegistration && values.password.length < 8) {
      nextErrors.password = "Password must be at least 8 characters."
    } else if (!values.password || values.password.length > 128) {
      nextErrors.password = "Enter a password of up to 128 characters."
    }

    if (isRegistration && values.phone.length > 15) {
      nextErrors.phone = "Phone number must be 15 characters or fewer."
    }

    if (isRegistration && values.confirmPassword !== values.password) {
      nextErrors.confirmPassword = "Passwords do not match."
    }

    setErrors(nextErrors)
    return Object.keys(nextErrors).length === 0
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    const isValid = validate()

    if (!isValid) {
      setNotice("")
      return
    }

    if (isRegistration) {
      try {
        setNotice("Creating your account...")

        const user = await authService.register({
          name: values.name,
          email: values.email,
          password: values.password,
          phone: values.phone,
        })

        setNotice("Registration successful! You can now log in.")
      } catch (error) {
        setNotice(error.message)
      }
    } else {
      try {
        setNotice("Logging in...")

        const result = await authService.login({
          email: values.email,
          password: values.password,
        })

        tokenService.save(result.access_token)
        const user = await authService.getMe(tokenService.get())

        console.log("Logged-in user:", user)
        setNotice("Login successful!")
        console.log("Login response:", result)
      } catch (error) {
        setNotice(error.message)
      }
    }
  }

  const fieldError = (name) =>
    errors[name] && (
      <span className="auth-field-error" id={`${name}-error`}>
        {errors[name]}
      </span>
    )
  const firstError = Object.values(errors).find(Boolean)

  return (
    <form className="auth-form" onSubmit={handleSubmit} noValidate>
      {isRegistration && (
        <label className="auth-field">
          <span>Name</span>
          <input
            autoComplete="name"
            name="name"
            value={values.name}
            onChange={updateValue}
            minLength={2}
            maxLength={100}
            required
            aria-invalid={Boolean(errors.name)}
            aria-describedby={errors.name ? "name-error" : undefined}
          />
          {fieldError("name")}
        </label>
      )}

      <label className="auth-field">
        <span>Email</span>
        <input
          type="email"
          autoComplete="email"
          name="email"
          value={values.email}
          onChange={updateValue}
          maxLength={150}
          required
          aria-invalid={Boolean(errors.email)}
          aria-describedby={errors.email ? "email-error" : undefined}
        />
        {fieldError("email")}
      </label>

      {isRegistration && (
        <label className="auth-field">
          <span>
            Phone <small>Optional</small>
          </span>
          <input
            type="tel"
            autoComplete="tel"
            name="phone"
            value={values.phone}
            onChange={updateValue}
            maxLength={15}
            aria-invalid={Boolean(errors.phone)}
            aria-describedby={errors.phone ? "phone-error" : undefined}
          />
          {fieldError("phone")}
        </label>
      )}

      <label className="auth-field">
        <span>Password</span>
        <span className="auth-password-control">
          <input
            type={passwordVisible ? "text" : "password"}
            autoComplete={isRegistration ? "new-password" : "current-password"}
            name="password"
            value={values.password}
            onChange={updateValue}
            minLength={isRegistration ? 8 : undefined}
            maxLength={128}
            required
            aria-invalid={Boolean(errors.password)}
            aria-describedby={errors.password ? "password-error" : undefined}
          />
          <button
            className="auth-password-toggle"
            type="button"
            aria-label={passwordVisible ? "Hide password" : "Show password"}
            aria-pressed={passwordVisible}
            onClick={() => setPasswordVisible((visible) => !visible)}>
            {passwordVisible ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        </span>
        {fieldError("password")}
      </label>

      {isRegistration && (
        <label className="auth-field">
          <span>Confirm password</span>
          <span className="auth-password-control">
            <input
              type={confirmationVisible ? "text" : "password"}
              autoComplete="new-password"
              name="confirmPassword"
              value={values.confirmPassword}
              onChange={updateValue}
              maxLength={128}
              required
              aria-invalid={Boolean(errors.confirmPassword)}
              aria-describedby={
                errors.confirmPassword ? "confirmPassword-error" : undefined
              }
            />
            <button
              className="auth-password-toggle"
              type="button"
              aria-label={
                confirmationVisible
                  ? "Hide confirmation password"
                  : "Show confirmation password"
              }
              aria-pressed={confirmationVisible}
              onClick={() => setConfirmationVisible((visible) => !visible)}>
              {confirmationVisible ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          </span>
          {fieldError("confirmPassword")}
        </label>
      )}

      <button className="primary-button auth-submit" type="submit">
        {isRegistration ? "Create account" : "Log in"}
      </button>
      <div
        className="auth-form-message"
        aria-live="polite"
        role={firstError ? "alert" : "status"}>
        {firstError || notice}
      </div>
    </form>
  )
}

export default AuthForm
