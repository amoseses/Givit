# GiftBrain AI (v2 – Feedback Ready)

This version supports explicit feedback collection for pre-launch training and includes a deployment preview UX before saving deployment URLs.

## Run
```bash
npm install
node API/index.js
```

Then open `http://localhost:3000` for the deployment preview tool.

## Deployment config
- Deployments list (default): `config/deployments.json`
- Deployment preview/save settings: `config/deployment-settings.json`
- Override paths with env vars:
  - `DEPLOYMENTS_CONFIG_PATH`
  - `DEPLOYMENT_SETTINGS_PATH`

### Settings
- `verifyBeforeSave`: if `true`, a deployment must be reachable and return 2xx before being saved.
- `requestTimeoutMs`: timeout used while previewing/verifying a deployment.

## Endpoints
- `POST /recommend`
- `POST /feedback`
- `GET /deployments`
- `POST /deployments/preview`
- `POST /deployments`
