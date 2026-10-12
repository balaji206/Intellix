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
export class RagError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

export async function indexDocument(file: {
  buffer: Buffer;
  originalname: string;
  mimetype: string;
}) {
  const form = new FormData();
  form.append(
    "file",
    new Blob([new Uint8Array(file.buffer)], { type: file.mimetype }),
    file.originalname
  );

  const res = await fetch(`${env.RAG_SERVICE_URL}/index`, {
    method: "POST",
    body: form,
    signal: AbortSignal.timeout(120000),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new RagError(res.status, (data as any).detail ?? "Indexing failed");
  return data;
}

export async function askQuestion(question: string, limit: number) {
  const res = await fetch(`${env.RAG_SERVICE_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, limit }),
    signal: AbortSignal.timeout(120000),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new RagError(res.status, (data as any).detail ?? "Question failed");
  return data;
}
