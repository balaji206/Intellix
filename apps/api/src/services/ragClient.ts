import { env } from "../config/env";

export async function getRagHealth(): Promise<{ ok: boolean; data?: unknown }> {
  try {
    const res = await fetch(`${env.RAG_SERVICE_URL}/health`, {
      signal: AbortSignal.timeout(3000),
    });
    const data = await res.json();
    return { ok: res.ok, data };
  } catch {
    return { ok: false };
  }
}