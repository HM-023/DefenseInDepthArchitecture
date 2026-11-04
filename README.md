![Defense in Depth Architecture](assets/cover.svg)

# Defense in Depth Architecture

**Local policy analysis workspace** · [User guide](docs/workspace-guide.md) · [Architecture](docs/workspace-architecture.md) · [Verification](docs/workspace-verification.md) · [Portfolio](https://github.com/HM-023)

[![Workspace verification](https://github.com/HM-023/DefenseInDepthArchitecture/actions/workflows/workspace.yml/badge.svg)](https://github.com/HM-023/DefenseInDepthArchitecture/actions/workflows/workspace.yml)

First-match evaluation over modeled zones, tcp/udp and ports with implicit default deny. The repository now includes a working, browser-based local workspace with a responsive dashboard and persistent records.

## What you can do

| Capability | Working behavior |
|:---|:---|
| **Ordered rule engine** | First-match evaluation over modeled zones, tcp/udp and ports with implicit default deny. |
| **Decision matrix** | Inspect inter-zone allow/deny results for a selected protocol and port. |
| **Rule review** | Flag rules fully shadowed by an earlier rule and broad management-access patterns. |
| **Executable assertions** | Declare expected flow decisions and inspect pass/fail results with the matching rule. |
| **Saved policy analyses** | Persist full input policies, matrices, assertions and warnings in SQLite. |
| **Reference layout** | Keep the original 11-node generic EVE-NG inventory and XML validator. |

## Run locally

Requires **Python 3.11+**. Run commands from this repository's root:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m webapp.app
```

Open **http://127.0.0.1:8103** in your browser. Stop the server with `Ctrl+C`.

Four workspaces use only Python's standard library. The ML workspace uses the packages in `requirements.txt`. The browser UI loads no external fonts, scripts, analytics or services. After dependencies are installed, the applications run offline.

For a different local port or data directory:

```bash
python -m webapp.app --port 8203 --data-dir path/to/local-workspace
```

## Architecture

![Local workspace architecture](assets/architecture.svg)

The server binds to loopback, checks the Host header and requires a fresh per-process token for API access. Mutations also reject foreign browser origins. Local data lives under `data/` by default; database files, model files and generated outputs are excluded from version control.

## Verify the implementation

```bash
python -m unittest discover -s tests -v
```

The [workspace workflow](https://github.com/HM-023/DefenseInDepthArchitecture/actions/workflows/workspace.yml) runs domain tests and an automated browser journey on GitHub. Browser runs upload real desktop and mobile captures as the **workspace-screenshots** artifact. See the verification document for the exact tested boundaries.

## Implementation boundaries

Policy reasoning is logical and zone-based. It does not simulate packets, install firewall rules, model stateful sessions or implement IDS, VPNs or routing. The EVE-NG layout still requires compatible images and device configurations.

These are local portfolio applications, with documented scope and tested workflows. They are not deployed enterprise services. No synthetic model score is presented as a real-world detection benchmark, and no generated network diagram or policy decision is presented as live network evidence.

## Repository map

| Path | Purpose |
|:---|:---|
| `webapp/app.py` | Application actions and local workspace state |
| `webapp/runtime.py` | Loopback HTTP boundary and SQLite document storage |
| `webapp/static/` | Responsive dashboard, forms, tables, charts and exports |
| `tests/` | Domain, persistence, server-boundary and browser checks |
| `docs/workspace-guide.md` | Usage, input formats and local-data operations |
| `docs/reference-case-study.md` | Prior case study, historical context and attribution |

## Provenance and reuse

The workspace code and generic examples are newly authored. Historical collaborative source materials, private datasets, credentials and organization-specific documents remain excluded. The [reference case study](docs/reference-case-study.md), [publication notes](PUBLICATION_NOTES.md) and existing security guidance retain the original contribution and reuse boundaries. No blanket license has been added to historical material.
