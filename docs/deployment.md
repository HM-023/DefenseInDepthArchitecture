# Reference layout and reproduction

The included layout is a newly authored, fictional example with 11 nodes and 10 isolated network objects. It illustrates a headquarters edge, a core, management/users/DMZ/logging endpoints and two branches. It does not reproduce the original shared lab.

1. Inspect `topology/inventory.json` and run `python topology/validate_topology.py`.
2. Supply your own compatible, legally obtained Cisco IOL image in EVE-NG. Replace `REPLACE_WITH_LICENSED_IOL_IMAGE.bin` in each router node with its installed image name. Endpoint nodes use the VPCS template.
3. Import `topology/example-topology.unl` into an isolated EVE-NG environment. Import compatibility and device boot are unverified.
4. Check all interface assignments before starting nodes. There are no external `pnet` connections in the example.
5. Configure addressing, routing and security policy yourself. No startup configurations are supplied. The external-test endpoint is an isolated test host.
6. Collect independent allow/deny tests, route tables, log delivery and failure/recovery evidence.

Routers and VPCS endpoints are placeholders for exploring segmentation. A VPCS endpoint is not a server or collector implementation. IPsec, IDS/IPS, AAA, HA and centralized logging remain design objectives; the layout does not implement them. This is not a one-command deployed lab.
