# Lighty Dogfood Plugin

Drive the Lighty platform from your own Claude: point it at a dataset and get
back the workflows it discovers, what drives the outcomes, and a report — all
explained in plain language. This is a **v0 dogfood** (pipeline-grade results),
so expect rough edges and tell us what's missing.

## What you need

1. **Claude Code** (or Claude Desktop with plugin support).
2. **A Lighty account** in the Lighty WorkOS organization (the same one you use for
   the Lighty dashboard). There's no token or URL to set — Claude signs you in through
   your browser. Not sure you're in the org? Ask the Lighty team.

## Setup (one time)

### Step 1 — Install the plugin

The `lighty-dogfood` plugin is published in a **public marketplace**
([`LightyAI/lighty-plugins`](https://github.com/LightyAI/lighty-plugins)), so
there's nothing to clone or download — you add the marketplace by name and install.
The steps differ slightly between Claude Code and Claude Desktop.

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
typing a marketplace name into chat — but it reads the **same** marketplace registry
as the Claude Code CLI on the same machine. So register the marketplace once from
your terminal, then install from Desktop:

1. Register the marketplace (one line in your terminal):
   ```bash
   claude plugin marketplace add LightyAI/lighty-plugins
   ```
   No CLI installed? Run `npm install -g @anthropic-ai/claude-code` first — it's the
   simplest way to register the marketplace that Desktop can then see.
2. In Claude Desktop, open **Plugins** — the Lighty plugin is listed under **Code**.
   Find **lighty-dogfood** there and install it.
3. Connect the server so it can sign you in: go to **Plugins → Connectors**, find
   **lighty-platform**, and click **Connect**. This opens the WorkOS sign-in in your
   browser (Step 2 below).
4. If the Lighty tools don't appear, **restart Claude Desktop**.

> Installing the plugin alone does **not** connect the MCP server — without the
> **Connectors → Connect** step, `lighty-platform` won't show up in Claude's MCP list.

> **Maintainers:** the canonical source for this plugin is
> [`LightyAI/lightly-core`](https://github.com/LightyAI/lightly-core) under
> `plugins/lighty-dogfood/`. The public
> [`LightyAI/lighty-plugins`](https://github.com/LightyAI/lighty-plugins) marketplace
> is **generated from it** by CI on every merge to `main` (see
> `.github/workflows/sync-plugins-marketplace.yml`) — edit the source here, never the
> published copy. To test a local working copy, point the marketplace at your checkout:
> `/plugin marketplace add /path/to/lightly-core/plugins`.

### Step 2 — Sign in with WorkOS

The first time Claude connects to Lighty, it opens a **WorkOS sign-in** in your
browser — sign in with your Lighty account and approve. That's it: there's no token
to copy or URL to set. (You must be a member of the Lighty WorkOS organization — the
same one you use for the Lighty dashboard; ask the Lighty team if you're not sure.)

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
