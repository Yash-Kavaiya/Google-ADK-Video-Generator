import os
import sys
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Get absolute path to the manim_server.py script
PATH_TO_YOUR_MCP_SERVER_SCRIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    "manim_server.py"
)

# Get the target folder path (parent directory)
TARGET_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

# Determine the Python executable to use
# Use the same Python that's running this script
PYTHON_EXECUTABLE = sys.executable

# Timeout for MCP operations (25 minutes = 1500 seconds)
# Manim can take time to render complex animations
MCP_TIMEOUT = 1500.0
from . import prompt
from . import google_prompt
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='manim_video_generator_agent',
    instruction=google_prompt.GOOGLE_THEMED_MANIM_VIDEO_GENERATOR,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=PYTHON_EXECUTABLE,
                    args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT],
                ),
                timeout=MCP_TIMEOUT,  # 25 minutes timeout for Manim rendering
            ),
        ),
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='npx',
                    args=[
                        "-y",  
                        "@modelcontextprotocol/server-filesystem",
                        os.path.abspath(TARGET_FOLDER_PATH),
                    ],
                ),
                timeout=MCP_TIMEOUT,  # 25 minutes timeout
            ),
        )
    ],
)