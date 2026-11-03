/*
 * Utilidades compartidas para autenticación JWT.
 *
 * - Añade el access token a las peticiones.
 * - Si el access token expiró, intenta refrescarlo una sola vez y reintenta.
 * - Si el refresh token ya no es válido, limpia la sesión y redirige al login.
 */
(function () {
  "use strict";

  const ACCESS_KEY = "access_token";
  const REFRESH_KEY = "refresh_token";
  const USER_KEY = "user_info";
  const LOGIN_URL = "/";

  // Evita que varias peticiones simultáneas disparen varios refresh a la vez.
  let refreshPromise = null;

  function getAccessToken() {
    return localStorage.getItem(ACCESS_KEY);
  }

  function getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY);
  }

  function clearSession() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(USER_KEY);
  }

  function redirectToLogin() {
    if (window.location.pathname !== LOGIN_URL) {
      window.location.href = LOGIN_URL;
    }
  }

  async function refreshAccessToken() {
    const refresh = getRefreshToken();
    if (!refresh) return null;

    if (!refreshPromise) {
      refreshPromise = fetch("/api/token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh }),
      })
        .then(async (response) => {
          if (!response.ok) return null;

          const data = await response.json();
          if (!data.access) return null;

          localStorage.setItem(ACCESS_KEY, data.access);
          // Con ROTATE_REFRESH_TOKENS el backend devuelve un refresh nuevo.
          if (data.refresh) {
            localStorage.setItem(REFRESH_KEY, data.refresh);
          }
          return data.access;
        })
        .catch(() => null)
        .finally(() => {
          refreshPromise = null;
        });
    }

    return refreshPromise;
  }

  async function apiFetch(url, options = {}, reintentar = true) {
    const headers = new Headers(options.headers || {});
    const access = getAccessToken();

    if (access) {
      headers.set("Authorization", `Bearer ${access}`);
    }
    if (typeof options.body === "string" && !headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }

    const response = await fetch(url, { ...options, headers });

    if (response.status === 401 && reintentar) {
      const nuevoAccess = await refreshAccessToken();

      if (nuevoAccess) {
        return apiFetch(url, options, false);
      }

      clearSession();
      redirectToLogin();
    }

    // Si el reintento con el token renovado también devuelve 401
    // (por ejemplo, porque el usuario fue desactivado), cerramos la sesión.
    if (response.status === 401 && !reintentar) {
      clearSession();
      redirectToLogin();
    }

    return response;
  }

  function requireAuth() {
    if (getAccessToken()) return true;
    redirectToLogin();
    return false;
  }

  async function logout() {
    const refresh = getRefreshToken();

    try {
      if (refresh) {
        // Invalida el refresh token en el servidor (blacklist).
        await fetch("/api/logout/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh }),
        });
      }
    } finally {
      clearSession();
      redirectToLogin();
    }
  }

  window.api = {
    apiFetch,
    requireAuth,
    logout,
    clearSession,
    getAccessToken,
  };
})();
