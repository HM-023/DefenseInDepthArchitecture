# Defense control validation matrix

| Layer | Example control | Evidence to collect in a safe lab | Status |
|---|---|---|---|
| Perimeter | Firewall default-deny + documented permitted services | Rule listing, allow/deny test records | Not verified |
| Internal | VLANs and inter-zone least-privilege | Host isolation test matrix | Not verified |
| Public services | DMZ separated from internal trusted network | Reachability tests from multiple zones | Not verified |
| Transport | Site-to-site IPsec | Tunnel status and packet counters | Not verified |
| Monitoring | IDS/IPS and central logs | Tagged test alerts, timestamps, retained logs | Not verified |
| Identity | Central AAA and MFA where appropriate | Authentication and privileged access tests | Not verified |
| Availability | HA firewalls, redundant links | Failover evidence and measured downtime | Not verified |
| Response | Alert escalation and documented containment | Tabletop exercise and closure records | Not verified |

**Rule:** An architectural element in a diagram is not the same as an implemented, validated security control.
