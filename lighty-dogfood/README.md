# Lighty Dogfood Plugin

Drive the Lighty platform from your own Claude: point it at a dataset and get
back the workflows it discovers, what drives the outcomes, and a report — all
explained in plain language. This is a **v0 dogfood** (pipeline-grade results),
so expect rough edges and tell us what's missing.

## What you need

1. **Claude Code** (or Claude Desktop with plugin support).
2. **A Lighty token** — the Lighty team gives you this. It's yours; don't share it.
   (You don't need an MCP URL — it's already baked into the plugin.)

## Setup (one time)

### Step 1 — Set your token

Set the token the Lighty team gave you as an environment variable so Claude can
authenticate:
```bash
export LIGHTY_MCP_TOKEN="<the token the Lighty team gave you>"
```
Put it in your shell profile (`~/.zshrc`, `~/.bashrc`) so it persists. The hosted
MCP URL (`https://app.lighty.ai`) is already baked into the plugin — you only set
the token.

### Step 2 — Install the plugin

This plugin is published in a **public marketplace**, so there's nothing to clone
or download — you add the marketplace by name and install. The steps differ
slightly between Claude Code and Claude Desktop.

**Claude Code (CLI)**

In a Claude Code session:
```
/plugin marketplace add LightyAI/lighty-plugins
/plugin install lighty-dogfood@lighty-plugins
```
Then activate it:
```
/reload-plugins
```
`/reload-plugins` connects the Lighty MCP server without a full restart; restarting
Claude Code works too.

Prefer your shell? The same two steps run non-interactively:
```bash
claude plugin marketplace add LightyAI/lighty-plugins
claude plugin install lighty-dogfood@lighty-plugins
```

**Claude Desktop**

Claude Desktop installs plugins from its built-in plugin browser rather than by
typing a marketplace name into chat — but it reads the **same** marketplace
registry as the Claude Code CLI on the same machine. So register the marketplace
once from your terminal, then install from Desktop:

1. Register the marketplace (one line in your terminal):
   ```bash
   claude plugin marketplace add LightyAI/lighty-plugins
   ```
   No CLI installed? Run `npm install -g @anthropic-ai/claude-code` first — it's the
   simplest way to register the marketplace that Desktop can then see.
2. In Claude Desktop, click the **+** next to the message box → **Plugins** →
   **Add plugin**.
3. Find **lighty-dogfood** in the list and install it (User scope is fine).
4. **Restart Claude Desktop** so the Lighty MCP server connects.

## Try it now — no data of your own needed

The instance ships with a **sample dataset**, so you can do a full run the moment
you've installed the plugin. Just say:

> **"Run the sample dataset through Lighty and tell me what you find."**

Claude finds the bundled sample (601 events from a few support agents working
customer tickets across Gmail, Salesforce, Zendesk, and a knowledge base), runs
the whole pipeline, and explains the workflows it discovered and what's associated
with slower cases — in plain business terms. A full run takes a few minutes; Claude
keeps you posted along the way.

## Use it

Then ask, in plain language:

- *"What can Lighty do right now?"* → Claude checks the connection and tells you.
- *"What sample datasets can I try?"* → lists the bundled samples.
- *"Run the sample dataset and explain what drives slower cases."*
- *"Show me the datasets that have already been analyzed."*
- *"Run the <dataset> analysis and explain what drives slow resolutions."*

Claude will inspect the data, run the analysis (this can take a few minutes — it
will keep you posted), and then explain the workflows it discovered, the patterns,
and what's associated with the outcomes — in business terms, not jargon.

## Bringing your own data (v0 note)

The hosted platform analyzes datasets that live **on the Lighty instance**, not
files on your laptop. For now:

- **Easiest:** run a bundled sample (above — "what sample datasets can I try?"). No
  setup, full end-to-end run.
- Explore datasets already staged on the instance ("show me the datasets").
- Your own file: upload it via the hosted Explorer UI (`https://app.lighty.ai/explorer.html`,
  drag-and-drop), then tell Claude the dataset name.
- Uploading a laptop file directly through chat isn't in v0 — if you want it, say so;
  it's on the roadmap.

## This is a dogfood — break it and tell us

It produces **pipeline-grade** results (discovered workflows + causal structure +
a basic report). The deeper customer-grade analytics (labor sizing, dollar-sized AI
recommendations, coverage framing) aren't in this version yet. When something feels
wrong, thin, or confusing, that's exactly the feedback we want.
