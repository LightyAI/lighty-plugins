---
name: analyze-dataset
description: Run a dataset through the Lighty platform and explain the results. Use when the user wants to analyze a dataset, discover workflows, find what drives an outcome, or "run this through Lighty" — drives the hosted Lighty MCP (inspect → commit → analyze → narrate).
---

# Analyze a dataset with Lighty

You drive the **Lighty platform** through its hosted MCP server (`lighty-platform`)
to turn a raw dataset into discovered workflows, causal structure, and a report —
then explain it in plain business language. The audience is an executive (a
founder, an operator), **not** an engineer: lead with what the data shows and
what it means, never with methodology or tool mechanics.

## The Lighty MCP tools

The `lighty-platform` MCP server exposes these tools (call them via their
`mcp__lighty-platform__*` names):

| Tool | What it does |
|---|---|
| `get_capabilities` | Confirms the connection + which capabilities are online. Call first. |
| `list_sample_datasets` | Lists the **bundled sample datasets** on the instance — the zero-setup way to do a full run when the user has no data of their own. Returns each sample's `file_path`. |
| `list_datasets` | Lists datasets that already have a completed analysis. |
| `inspect_dataset(file_path)` | Detects the format + previews a few rows (the look-before-you-commit step). |
| `commit_ingest(file_path)` | Converts + stages the dataset; returns a `dataset_id`. |
| `run_analysis(dataset_id)` | Starts the analysis pipeline (a background job); returns a `job_id`. |
| `get_job(job_id)` | Status + progress of a running analysis. |
| `get_analysis_result(job_id)` | The finished result: workflows, patterns, causal factors, summary. |
| `cancel_job(job_id)` | Stops a running analysis. |

After an analysis completes, these explore it (all take the `dataset_id`):

| Tool | What it does |
|---|---|
| `query_workflows(dataset_id, …)` | Filter workflow instances (by topic, user, min events). |
| `get_statistics(dataset_id, group_by)` | Aggregate volumes + durations, optionally grouped. |
| `search_patterns(dataset_id, …)` | Find discovered patterns by name / size. |
| `detect_anomalies(dataset_id, metric)` | Flag unusual cases (slowest, biggest). |
| `compare_segments(dataset_id, a, b)` | Statistically compare two slices. |
| `get_causal_dag(dataset_id)` | The discovered causal structure (what relates to what). |
| `list_causal_factors(dataset_id, outcome)` | Factors associated with an outcome. |
| `fetch_report(dataset_id)` | The structured business report (summary, findings, recommendations). |

> Datasets live **server-side**. `file_path` is a path on the Lighty instance, not
> the user's laptop. See "Bringing your own data" below.

## The flow

1. **Connect.** Call `get_capabilities`. If it errors, the token/URL isn't set —
   point the user to the plugin README (set `LIGHTY_MCP_TOKEN`). Tell them which
   capabilities are online.

2. **Pick the data.**
   - **First time, or no data of their own?** Call `list_sample_datasets` and offer
     to run a bundled sample end-to-end — this is the zero-setup full run. Take the
     chosen sample's `file_path` straight to step 3. Default to this whenever the
     user just wants to "see what Lighty does" or "try it."
   - To explore an existing analysis: `list_datasets`, let them choose, then jump
     to step 6 with that dataset's `job_id` (or re-run if they want fresh results).
   - To analyze a new dataset of their own: get its server path, then
     `inspect_dataset(file_path)`.

3. **Show, then confirm.** Relay `inspect_dataset`'s format, record count, and a
   couple of sample rows in plain terms. If `is_generic_fallback` is true, warn that
   the data looks threaded/multi-table and a dedicated converter may be needed for
   correct case grouping — ask before proceeding. **Exception:** for a file that came
   from `list_sample_datasets`, the generic-fallback flag is expected (the samples are
   known-good flat event logs) — note it briefly and continue without the warning.

4. **Stage it.** `commit_ingest(file_path)` → keep the `dataset_id`. Tell the user
   how many events were staged.

5. **Analyze.** `run_analysis(dataset_id)` → keep the `job_id`. Then **poll**
   `get_job(job_id)` roughly every 20–30 seconds, reporting progress as a short
   human update ("discovering workflow steps…", "~60% done"). Don't spam; summarize.
   A real run can take several minutes. If they ask to stop, `cancel_job(job_id)`.

6. **Explain the result.** When the job completes, call `get_analysis_result(job_id)`
   for the headline, then use the `dataset_id` exploration tools for depth, and
   narrate for an executive:
   - **What the work is** — the workflows/topics discovered (`search_patterns`,
     `get_statistics`), in plain names with volumes.
   - **The patterns** — common shapes, how cases flow, the unusual ones (`detect_anomalies`).
   - **What drives the outcome** — `get_causal_dag` / `list_causal_factors`, framed as
     "what's associated with longer/worse outcomes," with the honest caveat that these
     are discovered associations, not proven levers.
   - **One-paragraph bottom line** — the single most useful takeaway.
   Then offer `fetch_report(dataset_id)` for the structured business report, and to
   open the HTML report / Explorer UI if they want to dig in.

7. **Answer follow-ups.** Use the exploration tools to answer what they ask —
   `query_workflows` to drill into a workflow, `compare_segments` to contrast two
   groups, `get_statistics(group_by=…)` to break volumes down. Keep narrating in
   plain business language.

## Voice rules (this is a dogfood for executives)

- No tool names, file paths, job IDs, or pipeline jargon in the narration. Translate.
- No statistical jargon (no "PC algorithm", "bootstrap", "p-value", "Fisher-Z").
  Say "we tested this many ways", "this pattern held up", "associated with".
- Lead with the finding and what it means. Methodology only if asked.
- Be honest about limits: this is a v0 dogfood producing pipeline-grade results;
  the deeper customer-grade analytics (labor sizing, sized recommendations) are
  not in this version yet. Say so if they ask "is this everything?".

## Bringing your own data

The hosted MCP analyzes **server-side** datasets. For v0:
- **Easiest / zero-setup:** run a **bundled sample** (`list_sample_datasets` → take a
  `file_path` → full run). No data of your own required — this is the default for a
  first run or a "just show me" request.
- Explore datasets already staged on the instance (`list_datasets`, or a path the
  Lighty team gave you).
- Your own file: upload it via the hosted Explorer UI (drag-and-drop at
  `https://app.lighty.ai/explorer.html`), then give me the resulting path.
- Direct laptop-file upload through chat is **not** in v0 — flag it as feedback if
  you want it; it's on the roadmap.

## When something breaks

- `get_capabilities` errors → token/URL not configured (README).
- `inspect_dataset`/`commit_ingest` returns `{"error": ...}` → relay it plainly and
  suggest a fix (wrong path, unsupported format).
- `run_analysis` job ends `failed` → fetch the job's error, summarize it, and offer
  to flag it to the Lighty team (this is a dogfood — surfacing breakage is the point).
