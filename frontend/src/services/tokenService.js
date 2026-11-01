
const TOKEN_KEY = "api_craft_access_token";

export const tokenService = {
  save(token) {
    sessionStorage.setItem(TOKEN_KEY, token);
  },

  get() {
    return sessionStorage.getItem(TOKEN_KEY);
  },

  clear() {
    sessionStorage.removeItem(TOKEN_KEY);
  },
};
