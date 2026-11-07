# Changelog

## 2026-11-08

- Reworked the introduction around this project's design, code and verification, with a subject-specific diagram.
- Separated historical reference material from the later local application and removed unrelated cross-project boilerplate.
- Fixed SQLite transaction cleanup: connections now close after commit or rollback, preventing locked database files on Windows. Added regression checks for both exit paths.

## 1.0.0 — Local workspace release (2026-11-04)

- Ordered rule engine: First-match evaluation over modeled zones, tcp/udp and ports with implicit default deny.
- Decision matrix: Inspect inter-zone allow/deny results for a selected protocol and port.
- Rule review: Flag rules fully shadowed by an earlier rule and broad management-access patterns.
- Executable assertions: Declare expected flow decisions and inspect pass/fail results with the matching rule.
- Saved policy analyses: Persist full input policies, matrices, assertions and warnings in SQLite.
- Reference layout: Keep the original 11-node generic EVE-NG inventory and XML validator.
- Added a responsive local dashboard, request-boundary validation, ignored local state, regression tests and browser workflow verification.
- Preserved the prior case-study material and its contribution/reuse limitations.

Remaining scope: Policy reasoning is logical and zone-based. It does not simulate packets, install firewall rules, model stateful sessions or implement IDS, VPNs or routing. The EVE-NG layout still requires compatible images and device configurations.
