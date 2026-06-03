# Lighty Plugins

Public plugin marketplace for [Lighty AI](https://lighty.ai). Add it to Claude
Desktop (or Claude Code) to drive the Lighty platform from your own Claude — no
repo checkout required.

> **This directory is the source of truth.** The public
> [`LightyAI/lighty-plugins`](https://github.com/LightyAI/lighty-plugins) repo is
> **generated from this `plugins/` folder** by CI on every merge to `main` (see
> [`.github/workflows/sync-plugins-marketplace.yml`](../.github/workflows/sync-plugins-marketplace.yml)).
> Edit here, never the published repo. A consistency test
> (`workflow_engine/tests/test_plugin_marketplace_consistency.py`) gates `main` so
> the install commands, MCP URL, and auth model can't drift across the READMEs, the
> skill, and the website (`workflow_engine/ui/hub.html`).

## Install

**Claude Desktop** (default — no terminal needed): open **Customize → Plugins**, and
under **Personal plugins** click the small **+ → Create plugin → Add marketplace** and
enter `LightyAI/lighty-plugins`. Then **+ → Browse plugins**, find **lighty-dogfood**
(under **Code**) and **Install**, open the plugin's **Connectors → lighty-platform → Connect**,
and **restart Claude Desktop**. (The `/plugin` slash commands work only in Claude Code, not the Desktop chat.)
The [plugin README](./lighty-dogfood/README.md) has the step-by-step with screenshots.

**Claude Code (CLI):** in a Claude Code session —

```
/plugin marketplace add LightyAI/lighty-plugins
/plugin install lighty-dogfood@lighty-plugins
/reload-plugins
```

The first time Claude connects, it opens a **WorkOS sign-in** in your browser —
sign in with your Lighty account and approve. There's no token or URL to set; the
hosted MCP URL (`https://app.lighty.ai`) is baked into the plugin. You must be a
member of the Lighty WorkOS organization — ask the Lighty team if you're not sure.

## Plugins

| Plugin | What it does |
|--------|--------------|
| [**lighty-dogfood**](./lighty-dogfood/) | Point Claude at a dataset and get back discovered workflows, causal structure, and a plain-language report. v0 dogfood. See its [README](./lighty-dogfood/README.md) for full setup, including the Claude Desktop flow. |

## How it works

These plugins are thin — the compute lives in the hosted Lighty platform. Each
plugin bundles an MCP client that connects to `https://app.lighty.ai`; WorkOS
(browser sign-in, no token) authenticates you. See each plugin's README for details.
