import express from "express";
import cors from "cors";
import helmet from "helmet";
import { healthRouter } from "./routes/health";
import { documentsRouter } from "./routes/documents";
import type { NextFunction, Request, Response } from "express";
export const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());

app.use("/health", healthRouter);

app.use("/", documentsRouter);


app.use((err: any, _req: Request, res: Response, _next: NextFunction) => {
  if (err?.type === "entity.parse.failed") {
    return res.status(400).json({ error: "Invalid JSON body" });
  }
  if (err?.code === "LIMIT_FILE_SIZE") {
    return res.status(413).json({ error: "File too large (max 20 MB)" });
  }
  console.error(err);
  res.status(500).json({ error: "Internal server error" });
});