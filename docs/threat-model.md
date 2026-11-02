# Simplified threat model

**Protected assets:** internal applications, account management services, administrative interfaces, service data and cross-site traffic.

**Trust boundaries:** external-to-DMZ, external-to-internal, DMZ-to-internal, user-to-management, branch-to-branch and monitoring-to-managed devices.

**Threat categories:** unauthorized remote access, compromised user endpoints, lateral movement, spoofing, misconfigured policies, administrative credential compromise, and service availability loss.

**Mitigations:** deny-by-default cross-boundary policy, separate management plane, central AAA with MFA where supported, device configuration baselines, monitoring, timely patching, secure tunnels, tested backups and failover.

**Residual risk:** overprivileged firewall rules, blind spots in telemetry, shared credentials, outdated appliance images, incomplete validation and configuration drift.
