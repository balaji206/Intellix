import { Pool } from "pg";
import Redis from "ioredis";
import { env } from "./env";

export const pool = new Pool({
  host: env.POSTGRES_HOST,
  port: env.POSTGRES_PORT,
  user: env.POSTGRES_USER,
  password: env.POSTGRES_PASSWORD,
  database: env.POSTGRES_DB,
});

export const redis = new Redis({
  host: env.REDIS_HOST,
  port: env.REDIS_PORT,
  lazyConnect: true,
});