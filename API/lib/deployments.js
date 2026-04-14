import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const defaultConfigPath = path.resolve(__dirname, "../../config/deployments.json");
const defaultSettingsPath = path.resolve(__dirname, "../../config/deployment-settings.json");

const configPath = process.env.DEPLOYMENTS_CONFIG_PATH || defaultConfigPath;
const settingsPath = process.env.DEPLOYMENT_SETTINGS_PATH || defaultSettingsPath;

const defaultSettings = {
  verifyBeforeSave: true,
  requestTimeoutMs: 4000
};

function ensureJsonFile(filePath, defaultData) {
  if (!fs.existsSync(filePath)) {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, JSON.stringify(defaultData, null, 2));
  }
}

function readJson(filePath, fallback) {
  ensureJsonFile(filePath, fallback);
  const raw = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(raw);
}

function readConfig() {
  const parsed = readJson(configPath, { deployments: [] });
  if (!Array.isArray(parsed.deployments)) {
    parsed.deployments = [];
  }
  return parsed;
}

function readSettings() {
  const parsed = readJson(settingsPath, defaultSettings);
  return {
    ...defaultSettings,
    ...parsed
  };
}

function writeConfig(config) {
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
}

function normalizeUrl(input) {
  const raw = (input || "").trim();
  if (!raw) {
    throw new Error("Deployment URL is required.");
  }

  const withProtocol = /^https?:\/\//i.test(raw) ? raw : `https://${raw}`;
  const url = new URL(withProtocol);

  if (!["http:", "https:"].includes(url.protocol)) {
    throw new Error("Only HTTP/S URLs are supported.");
  }

  url.pathname = url.pathname.replace(/\/$/, "");
  return url.toString();
}

async function checkDeployment(url) {
  const settings = readSettings();
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), settings.requestTimeoutMs);

  try {
    const response = await fetch(url, {
      method: "GET",
      redirect: "follow",
      signal: controller.signal
    });

    return {
      reachable: true,
      ok: response.ok,
      status: response.status,
      finalUrl: response.url,
      warning: null
    };
  } catch (_error) {
    return {
      reachable: false,
      ok: false,
      status: null,
      finalUrl: url,
      warning: "Could not reach deployment from this server."
    };
  } finally {
    clearTimeout(timeout);
  }
}

function listDeployments() {
  return readConfig().deployments;
}

function saveDeployment({ name, url }) {
  const config = readConfig();
  const normalizedUrl = normalizeUrl(url);
  const entry = {
    id: Date.now().toString(36),
    name: (name || "Untitled deployment").trim(),
    url: normalizedUrl,
    addedAt: new Date().toISOString()
  };

  config.deployments.push(entry);
  writeConfig(config);

  return entry;
}

export {
  checkDeployment,
  configPath,
  listDeployments,
  normalizeUrl,
  readSettings,
  saveDeployment,
  settingsPath
};
