import sys
import os
import traceback
import requests
from typing import Any, List, Dict
from mcp.server.fastmcp import FastMCP
from notion_client import Client
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
class PRAnalyzer:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize MCP Server
        self.mcp = FastMCP(name="github_pr_analysis")
        print("MCP Server initialized", file=sys.stderr)

        
        # Register MCP tools
        self._register_tools()

    
    def _register_tools(self):
        """Register MCP tools for PR analysis."""   
        @self.mcp.tool()
        def add(a: int, b: int) -> int:
            """Add two numbers"""
            return a + b

        @self.mcp.tool()
        def multiply(a: int, b: int) -> int:
            """Multiply two numbers"""
            return a * b
        @self.mcp.tool()
        async def create_github_repo(name: str, description: str = "", private: bool = False) -> Dict[str, Any]:
            """Create a new GitHub repository.
            
            Args:
                name: Name of the repository
                description: Optional description of the repository
                private: Whether the repository should be private (default: False)
                
            Returns:
                Dictionary containing the created repository information
            """
            print(f"Creating GitHub repository: {name}", file=sys.stderr)
            try:
                headers = {
                    'Authorization': f'token {os.getenv("GITHUB_TOKEN")}',
                    'Accept': 'application/vnd.github.v3+json'
                }
                
                data = {
                    'name': name,
                    'description': description,
                    'private': private,
                    'auto_init': True  # Initialize with a README
                }
                
                response = requests.post(
                    'https://api.github.com/user/repos',
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                
                repo_info = response.json()
                print(f"Successfully created repository: {repo_info['html_url']}", file=sys.stderr)
                return {
                    'name': repo_info['name'],
                    'url': repo_info['html_url'],
                    'description': repo_info['description'],
                    'private': repo_info['private']
                }
            except Exception as e:
                error_msg = f"Error creating GitHub repository: {str(e)}"
                print(error_msg, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                return {'error': error_msg}
        
    
    def run(self):
        """Start the MCP server."""
        try:
            print("Running MCP Server for GitHub PR Analysis...", file=sys.stderr)
            self.mcp.run(transport="stdio")
        except Exception as e:
            print(f"Fatal Error in MCP Server: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    analyzer = PRAnalyzer()
    analyzer.run() 