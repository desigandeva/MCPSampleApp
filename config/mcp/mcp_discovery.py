import os
import json
from typing import Any

class MCPDiscovery:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = self.load_config()
        print(self.config)

    def load_config(self) -> dict[str, Any]:
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def get_servers(self) -> dict[str, Any]:
        return self.config.get("mcpServers", {})

# if __name__ == "__main__":
#     config_file = os.path.join(os.path.dirname(__file__), "config.json")
#     discovery = MCPDiscovery(config_file)
#     servers = discovery.get_servers()
#     print(servers)