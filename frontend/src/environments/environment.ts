/**
 * TaskFlow Frontend - Environment Configuration
 * JIRA Story: TFLOW-6 - [FE] Setup Angular project with routing
 */

export const environment = {
  production: false,
  // Use 127.0.0.1, not localhost: on this machine Docker/WSL holds the IPv6
  // (::1) side of port 8000, and browsers resolve localhost to ::1 first, so
  // requests land on the wrong service instead of uvicorn.
  apiUrl: 'http://127.0.0.1:8000/api'
};
