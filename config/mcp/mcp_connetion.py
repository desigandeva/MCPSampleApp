import asyncio
import json
import os
import datetime
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client


class FixedClientSession(ClientSession):
    """
    Fixed ClientSession that properly handles the timeout attribute.
    
    This works around a bug where _session_read_timeout_seconds is set
    as a function instead of a timedelta object.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ensure _session_read_timeout_seconds is a timedelta, not a function
        if not hasattr(self, '_session_read_timeout_seconds') or \
           callable(getattr(self, '_session_read_timeout_seconds', None)):
            self._session_read_timeout_seconds = datetime.timedelta(seconds=30)


async def run():
    # Discover servers from the config file
    config_file_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_file_path, "r") as f:
        config = json.load(f)

    # Get the tool metadata for all servers
    tool_metadata = {}
    for server_name, server_info in config["mcpServers"].items():
        try:
            print(f"\n{'='*60}")
            print(f"Connecting to: {server_name}")
            print(f"URL: {server_info['url']}")
            print(f"{'='*60}")
            
            async with streamablehttp_client(url=server_info["url"]) as streams:
                print(f"✓ Created streams")
                
                # Use FixedClientSession instead of ClientSession
                async with FixedClientSession(*streams) as session:
                    print(f"✓ Created session")
                    
                    await session.initialize()
                    print(f"✓ Initialized session")
                    
                    # list_tools() returns a list of Tool objects
                    tools = await session.list_tools()
                    tool_names = [tool.name for tool in tools.tools]
                    
                    print(f"✓ Found {len(tool_names)} tools: {tool_names}")
                    tool_metadata[server_name] = tool_names
                    
        except Exception as e:
            print(f"✗ Error loading tools from {server_name}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*60}")
    print("Tool Metadata Summary")
    print(f"{'='*60}")
    for server, tools in tool_metadata.items():
        print(f"{server}: {tools}")
    print(f"{'='*60}\n")

    # Example: Run a tool from the 'Calculater' server
    server_name = "Calculater"
    tool_name = "add"

    # Run a tool safely via a session
    if server_name in tool_metadata and tool_name in tool_metadata[server_name]:
        print(f"Running tool '{tool_name}' on server '{server_name}'...")
        server_info = config["mcpServers"][server_name]
        
        try:
            async with streamablehttp_client(url=server_info["url"]) as streams:
                # Use FixedClientSession instead of ClientSession
                async with FixedClientSession(*streams) as session:
                    await session.initialize()
                    
                    # Call tool with arguments wrapped in an 'input' dictionary
                    result = await session.call_tool(
                        tool_name, 
                        arguments={"input": {"x": 10, "y": 5}}
                    )
                    
                    print(f"✓ Result of {tool_name} on {server_name}:")
                    print(f"  {result}")
                    
        except Exception as e:
            print(f"✗ Error running tool {tool_name} on {server_name}: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"✗ Could not run tool: Server '{server_name}' or tool '{tool_name}' not available.")
        print(f"   Available servers: {list(tool_metadata.keys())}")
        if server_name in tool_metadata:
            print(f"   Available tools in {server_name}: {tool_metadata[server_name]}")


if __name__ == "__main__":
    asyncio.run(run())
