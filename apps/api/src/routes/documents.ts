import { Router } from "express";
import multer from "multer";
import { z } from "zod";
import { askQuestion, indexDocument, RagError } from "../services/ragClient";

export const documentsRouter = Router();

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 20 * 1024 * 1024 }, // 20 MB
});

const ALLOWED = [".pdf", ".docx", ".txt", ".md"];

documentsRouter.post("/documents", upload.single("file"), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "No file uploaded (field name: file)" });
  }
  const name = req.file.originalname.toLowerCase();
  if (!ALLOWED.some((ext) => name.endsWith(ext))) {
    return res.status(400).json({ error: `Allowed types: ${ALLOWED.join(", ")}` });
  }

  try {
    const result = await indexDocument(req.file);
    res.status(201).json(result);
    } catch (e) {
    if (e instanceof RagError) return res.status(e.status).json({ error: e.message });
    console.error("RAG call failed:", e);
    res.status(502).json({ error: "AI service unavailable" });
  }
});

const askSchema = z.object({
  question: z.string().min(1).max(2000),
  limit: z.number().int().min(1).max(20).default(5),
});

documentsRouter.post("/ask", async (req, res) => {
  const parsed = askSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: "Invalid request", details: parsed.error.flatten() });
  }

  try {
    const result = await askQuestion(parsed.data.question, parsed.data.limit);
    res.json(result);
  } catch (e) {
    if (e instanceof RagError) return res.status(e.status).json({ error: e.message });
    res.status(502).json({ error: "AI service unavailable" });
  }
});