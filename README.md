# nullvpn-web

Unified NullVPN website — works identically on **Web2**, **TON Web3**, and **any HTTP network**.

## Live Deployments

| Network | URL | Protocol |
|---|---|---|
| Web2 Clearnet | https://nullvpn.net | HTTPS |
| TON Web3 | https://nullvpn.ton.run | TON Storage |
| Telegram | https://t.me/nullvpnnet | Telegram |

## Channels
- Telegram: https://t.me/nullvpnnet
- Bot: https://t.me/nullvpnnetbot
- Web3: https://nullvpn.ton.run

## Static bootstrap profile (owner 2026-10-04)

| Path | Body |
|---|---|
| `/bootstrap` | tokenless bootstrap profile — base64 vless link list (PROD backup path) |
| `/bootstrap-dev` | same body at the DEV variant's backup path (`BOOTSTRAP_BACKUP_URL` in `config/dev.env`, PR #266; was 404 until r137) |
| `/sub/android` | same body at the app path (drop-in URL swap) |

- **Source of truth:** CF-worker route `bootstrap(-dev).nullvpn.net` (byte-identical body).
- **CI/CD:** `.github/workflows/publish-bootstrap.yml` — weekly cron + `workflow_dispatch` (optional `body_base64` input); validates base64→`vless://`, commits only on change, `nullvpn-bot` identity.
- **Why a static mirror:** the RU-side network path degrades all TLS to the Cloudflare edge (every CF HTTPS port stalls; http:80 is the only live CF path there). GitHub Pages rides Fastly/GitHub IPs and stays reachable from that path — verified 2026-10-04. The port-80 scheme law for `tunnel.sh` (owner 2026-10-04) is unchanged; this file is the tamper-resistant https mirror.
