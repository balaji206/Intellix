import { Router } from "express";
import { pool, redis } from "../config/db";
import { getRagHealth } from "../services/ragClient";

export const healthRouter = Router();

healthRouter.get("/", async (_req, res) => {
  const checks: Record<string, string> = {};

  try {
    await pool.query("SELECT 1");
    checks.postgres = "ok";
  } catch {
    checks.postgres = "down";
  }

  try {
    if (redis.status === "wait") await redis.connect();
    await redis.ping();
    checks.redis = "ok";
  } catch {
    checks.redis = "down";
  }

  const healthy = Object.values(checks).every((v) => v === "ok");
  res.status(healthy ? 200 : 503).json({
    status: healthy ? "ok" : "degraded",
    service: "intellix-api",
    checks,
  });
});


healthRouter.get("/all", async (_req, res) => {
  const checks: Record<string, unknown> = {};

  try {
    await pool.query("SELECT 1");
    checks.postgres = "ok";
  } catch {
    checks.postgres = "down";
  }

  try {
    if (redis.status === "wait") await redis.connect();
    await redis.ping();
    checks.redis = "ok";
  } catch {
    checks.redis = "down";
  }

  const rag = await getRagHealth();
  checks.ragService = rag.ok ? "ok" : "down";
  if (rag.data) checks.ragDetails = rag.data;

  const healthy = ["postgres", "redis", "ragService"].every((k) => checks[k] === "ok");
  res.status(healthy ? 200 : 503).json({
    status: healthy ? "ok" : "degraded",
    service: "intellix-api",
    checks,
  });
});