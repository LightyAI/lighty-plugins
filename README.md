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

Then set the token the Lighty team gave you:

```bash
export LIGHTY_MCP_TOKEN="<your token>"
```

(The hosted MCP URL, `https://app.lighty.ai`, is already baked into the plugin —
you only set the token. The token is per-user; don't share it.)

## Plugins

| Plugin | What it does |
|--------|--------------|
| [**lighty-dogfood**](./lighty-dogfood/) | Point Claude at a dataset and get back discovered workflows, causal structure, and a plain-language report. v0 dogfood. See its [README](./lighty-dogfood/README.md) for full setup, including the Claude Desktop flow. |

## How it works

These plugins are thin — the compute lives in the hosted Lighty platform. Each
plugin bundles an MCP client that connects to `https://app.lighty.ai`; your token
authenticates you. See each plugin's README for details.
