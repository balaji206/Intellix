import dotenv from "dotenv";
import path from "path";
import { z } from "zod";

// Load the .env file from the project root
dotenv.config({ path: path.resolve(__dirname, "../../../../.env") });

const schema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  API_PORT: z.coerce.number().default(4000),
  POSTGRES_USER: z.string(),
  POSTGRES_PASSWORD: z.string(),
  POSTGRES_DB: z.string(),
  POSTGRES_HOST: z.string().default("localhost"),
  POSTGRES_PORT: z.coerce.number().default(5432),
  REDIS_HOST: z.string().default("localhost"),
  REDIS_PORT: z.coerce.number().default(6379),
});

export const env = schema.parse(process.env);