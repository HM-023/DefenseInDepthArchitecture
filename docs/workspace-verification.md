# Workspace verification

## Automated domain and boundary checks

Run `python -m unittest discover -s tests -v` from the repository root. The suite contains 15 tests, including HTTP boundary and SQLite storage checks. Policy checks cover ordered first-match decisions, implicit deny, shadowed rules, invalid inputs and saved analyses.

The implementation was exercised locally on 2026-11-04. Final hosted results are available in [Workspace verification](https://github.com/HM-023/DefenseInDepthArchitecture/actions/workflows/workspace.yml); inspect the commit associated with each run. The workflow additionally runs the browser journey and uploads desktop/mobile captures. A green unit-test job alone is not evidence that a browser job passed.

## Boundaries

These checks establish logical policy behavior, not live firewall enforcement, simulator import, encrypted tunnels or IDS/IPS operation.

## Browser journey

`tests/browser.cjs` starts an isolated server using a temporary data directory, uses real browser controls to exercise the main workflow, checks for JavaScript errors, captures 1440-pixel desktop and 390-pixel mobile views, tests viewport overflow and reloads saved state. The temporary test data is deleted afterward. To run it locally with Node 22+:

```bash
npm install --no-save --package-lock=false playwright@1.56.1
npx playwright install chromium
node tests/browser.cjs
```

The application itself needs neither Node nor Playwright. These are verification dependencies only.

## Hosted release check

On 2026-11-04, both the domain/unit job and browser workflow passed for the [local workspace release](https://github.com/HM-023/DefenseInDepthArchitecture/actions/runs/41802140103). The repository screenshots were captured by that successful browser journey. Use the workflow link above to inspect subsequent commits and results.

## Local Windows check — 2026-11-08

All 15 tests passed with Python 3.13.4 after fixing SQLite connection cleanup. The new regression checks verify that successful and failed transactions close their connections, and that failed writes roll back. Previously, transaction exit left connections open, which locked database files on Windows.

The existing browser journey also passed locally on 2026-11-08 using Node 22.16.0, bundled Playwright 1.62.1 and the already-installed Chromium headless shell (revision 1243). A local runner supplied the browser executable path; repository tests and CI's pinned Playwright 1.56.1 configuration were unchanged. The journey exercised the app workflow, captured desktop/mobile views, checked viewport overflow and reloaded persisted state. Inputs were fictional or synthetic.

These are local execution results. Historical hosted checks remain recorded above; subsequent hosted runs should be inspected against their commit.
