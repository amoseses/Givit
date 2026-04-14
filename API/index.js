import express from "express";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import gifts from "../data/gift_taxonomy.json" with { type: "json" };
import { recommend } from "../engine/recommender.js";
import {
  checkDeployment,
  configPath,
  listDeployments,
  normalizeUrl,
  readSettings,
  saveDeployment,
  settingsPath
} from "./lib/deployments.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json());
app.use(express.static(path.resolve(__dirname, "../public")));

app.post("/recommend", (req, res) => {
  const profile = req.body;
  const results = recommend(profile, gifts);
  res.json(results);
});

app.post("/feedback", (req, res) => {
  const record = {
    timestamp: new Date().toISOString(),
    ...req.body
  };

  fs.appendFileSync("./feedback_log.jsonl", JSON.stringify(record) + "\n");

  res.sendStatus(200);
});

app.get("/deployments", (_req, res) => {
  res.json({
    configPath,
    settingsPath,
    settings: readSettings(),
    deployments: listDeployments()
  });
});

app.post("/deployments/preview", async (req, res) => {
  try {
    const normalizedUrl = normalizeUrl(req.body?.url);
    const check = await checkDeployment(normalizedUrl);

    res.json({
      requestedUrl: req.body?.url,
      normalizedUrl,
      ...check
    });
  } catch (error) {
    res.status(400).json({
      error: error.message || "Unable to preview deployment."
    });
  }
});

app.post("/deployments", async (req, res) => {
  try {
    const normalizedUrl = normalizeUrl(req.body?.url);
    const settings = readSettings();
    const check = await checkDeployment(normalizedUrl);

    if (settings.verifyBeforeSave && (!check.reachable || !check.ok)) {
      const details = check.warning || `Deployment responded with status ${check.status}.`;
      return res.status(400).json({
        error: `${details} Fix it before adding or set verifyBeforeSave=false in settings.`
      });
    }

    const entry = saveDeployment({
      name: req.body?.name,
      url: normalizedUrl
    });

    res.status(201).json({
      deployment: entry,
      check
    });
  } catch (error) {
    res.status(400).json({
      error: error.message || "Unable to add deployment."
    });
  }
});

app.listen(3000, () => {
  console.log("GiftBrain v2 running on :3000");
  console.log(`Deployment config: ${configPath}`);
  console.log(`Deployment settings: ${settingsPath}`);
});
