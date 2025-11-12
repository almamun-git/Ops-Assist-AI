export const STORAGE_KEY = "opsai_api_base";

export function getStoredApiBase(): string | null {
  if (typeof window === "undefined") return null;
  try {
    return localStorage.getItem(STORAGE_KEY);
  } catch {
    return null;
  }
}

export function setStoredApiBase(url: string) {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(STORAGE_KEY, url);
  } catch {}
}

export function getApiBase(): string {
  const envBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const stored = getStoredApiBase();
  const base = (stored || envBase).replace(/\/+$/, "");
  return base;
}

export function getDocsUrl(): string {
  return `${getApiBase()}/docs`;
}
