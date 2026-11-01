const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(
  /\/+$/,
  "",
)

//Handles HTTP requests and backend errors.
async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  })

  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = data.detail
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg).join(", ")
      : typeof detail === "string"
        ? detail
        : "Request failed Please try again."
    throw new Error(message)
  }
  return data
}
export const authService = {
  register({ name, email, password, phone }) {
    return request("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        name: name.trim(),
        email: email.trim(),
        password,
        phone: phone.trim() || null,
      }),
    })
  },
  login({ email, password }) {
    return request("/auth/login", {
      method: "POST",
      body: JSON.stringify({
        email: email.trim(),
        password,
      }),
    })
  },
  getMe(token) {
    return request("/auth/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  },
}
