# Lighty Plugins

Public plugin marketplace for [Lighty AI](https://lighty.ai). Add it to Claude
Code (or Claude Desktop) to drive the Lighty platform from your own Claude — no
repo checkout required.

## Install

In a Claude Code session:

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
