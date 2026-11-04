# Defense in Depth Architecture: workspace guide

## Start and stop

Use `python -m webapp.app` from the repository root and open the printed loopback address. Python 3.11 or later is the supported baseline. Use the virtual environment activation command for your operating system. The default port is 8103; `--port` changes it. `Ctrl+C` shuts down the server.

## Main workflow

1. Inspect or edit the example policy JSON. Zone names are case-sensitive. `any` is a reserved wildcard. Provide 2–20 zones, up to 250 ordered rules and up to 250 flow assertions.
2. A rule contains an ID, source zone, destination zone, tcp/udp/any protocol, numeric port or `any`, and allow/deny action. First match wins. No match means deny. Rule IDs must be unique.
3. Declare expected allow/deny decisions in `tests`. Test flows need concrete zones, tcp or udp, and a port. Set `matrix_protocol` and `matrix_port` to inspect another service.
4. Analyze the policy. Inspect actual decisions, matching rule IDs, failed assertions and review warnings. A shadowing warning means an earlier single rule fully covers a later rule; combinations of earlier rules are not analyzed for union coverage.
5. Broad-allow and internet-to-management warnings are rule-pattern heuristics. They are not evidence that an actual management service is exposed. The heuristic names the `internet` and `management` zones in the reference vocabulary; custom zone names require your own assertions.
6. Save and export analyses. The matrix deliberately excludes same-zone traffic. Stateful behavior, NAT, direction-dependent sessions, routing and multiple-rule composition are outside this logical model.

## Local data and backups

Records live in `data/workspace.sqlite3` by default. ML model artifacts additionally live in `data/models/`. These paths are excluded from git. The file formats contain local workspace information and are not encrypted by the application. Stop the server before copying the entire data directory for a simple backup, then use `--data-dir` to reopen that copy. Deleting the data directory while the server is stopped resets the workspace. Exported files are saved wherever the browser downloads them; this app does not automatically publish them.

## Local browser boundary

Use the exact printed localhost/127.0.0.1 URL and reload after restarting the server. A new random session token is issued each time. There is no remote bind option. Host checks resist DNS rebinding, and API requests require the page's token. This is a browser-request boundary, not account authentication and not a defense against other software already running as the same operating-system user.

## Browser verification

GitHub Actions runs the end-to-end journey in `tests/browser.cjs` using pinned Playwright 1.56.1. It exercises real forms and local API actions, checks browser errors and mobile viewport fit, reloads persisted state and captures desktop/mobile PNGs. Screenshots use only synthetic or fictional inputs.
