"""Static checks for a generic EVE-NG XML layout (does not run the lab)."""
from collections import Counter
from pathlib import Path
import json
import xml.etree.ElementTree as ET


def main():
    base = Path(__file__).resolve().parent
    root = ET.parse(base / "example-topology.unl").getroot()
    nodes, networks = root.findall(".//node"), root.findall(".//network")
    node_ids = [n.get("id") for n in nodes]
    network_ids = [n.get("id") for n in networks]
    node_names = [n.get("name") for n in nodes]
    assert all(node_ids) and len(set(node_ids)) == len(node_ids), "Duplicate/missing node IDs"
    assert all(network_ids) and len(set(network_ids)) == len(network_ids), "Duplicate/missing network IDs"
    assert all(node_names) and len(set(node_names)) == len(node_names), "Duplicate/missing node names"
    network_set = set(network_ids)
    interfaces = root.findall(".//interface")
    dangling = [(item.get("name"), item.get("network_id")) for item in interfaces
                if item.get("network_id") and item.get("network_id") not in network_set]
    assert not dangling, f"Dangling interface links: {dangling[:10]}"
    inventory = json.loads((base / "inventory.json").read_text(encoding="utf-8"))
    assert len(nodes) == inventory["node_count"], "Inventory node count mismatch"
    assert len(networks) == inventory["network_objects"], "Inventory network count mismatch"
    assert dict(Counter(n.get("type", "unknown") for n in nodes)) == inventory["virtualization_counts"]
    print(f"Layout checks passed: {len(nodes)} nodes, {len(networks)} network objects, "
          f"{len(interfaces)} interfaces; zero dangling network links")


if __name__ == "__main__":
    main()
