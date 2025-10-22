Here is a comprehensive `README.md` for your repository, including a Mermaid diagram that details the project's architecture, based on the files you provided.

-----

# Google ADK Video Generator

This project is an agent built with the **Google Agent Development Kit (ADK)** designed to automatically generate high-quality, Google-themed animated videos from text prompts. It uses **Manim**, a powerful programmatic animation engine, to create these videos, ensuring they adhere to Google's Material Design principles and official brand colors.

## Features

  * **Text-to-Video Generation:** Converts natural language prompts into complete animated videos.
  * **Google-Themed Design:** Strictly enforces Google's Material Design aesthetic, using the official brand color palette (`GOOGLE_BLUE`, `GOOGLE_RED`, `GOOGLE_YELLOW`, `GOOGLE_GREEN`), fonts, and layout principles.
  * **Dual-Format Support:** Capable of generating videos in both **horizontal (16:9)** for YouTube and **vertical (9:16)** for Shorts/Reels.
  * **Agentic Workflow:** Uses an `LlmAgent` to understand requests, write Manim code, and control the video generation process.
  * **MCP Tool Integration:** Leverages the Model-Context-Protocol (MCP) to provide the agent with custom tools for executing Manim code and managing files.

-----

## Architecture

The agent's architecture is built around the Google ADK, which coordinates an LLM with various tools via MCP servers.

```mermaid
flowchart TD
    subgraph "User Interaction"
        User[End User]
    end

    subgraph "Google ADK Agent"
        User -- "Prompt (e.g., 'Create a reel about...')" --> Agent
        Agent[LlmAgent: manim_video_generator_agent]
        Agent -- "Guides LLM with prompt" --> SystemPrompt(google_prompt.py)
        Agent -- "Uses Model" --> LLM[LLM: Claude 3.5 Sonnet]
    end

    subgraph "Agent Tools (via MCP)"
        Agent -- "Tool Call" --> MCPTools(MCP Toolsets)
        MCPTools --> FilesystemServer[Filesystem MCP Server<br>@modelcontextprotocol/server-filesystem]
        MCPTools --> ManimServer[Manim MCP Server<br>manim_server.py]
    end

    subgraph "Execution Environment"
        ManimServer -- "Calls Tool" --> ExecManim(execute_manim_code)
        ExecManim -- "Writes code" --> TempFile(scene.py)
        ExecManim -- "Runs command" --> ManimCLI[subprocess.run('manim -p scene.py')]
        ManimCLI -- "Renders video" --> VideoFile[Video File (.mp4)<br>in /media]
    end

    Agent -- "Returns video path" --> User
```

-----

## How It Works

1.  **User Prompt:** A user sends a request to the agent, such as "Create a short vertical video explaining Google's AI Principles."
2.  **Agent & LLM:** The `LlmAgent` (`manim_video_generator_agent`) receives the prompt. It uses the detailed instructions in `my_agent/google_prompt.py` to guide the **Anthropic Claude 3.5 Sonnet** model.
3.  **Code Generation:** The LLM generates Python code for Manim, specifically designed to match the Google Material aesthetic (colors, fonts, layout, and animations) as defined in the prompt.
4.  **Tool Call:** The agent invokes the `execute_manim_code` tool from its `MCPToolset`.
5.  **Manim Server:** This tool call is routed to the custom `my_agent/manim_server.py`. This server writes the received Manim code to a temporary `scene.py` file.
6.  **Video Rendering:** The server executes the Manim code using `subprocess.run`. Manim renders the animation and saves the final video file (e.g., `.mp4`) to the `my_agent/media/` directory.
7.  **File Management:** The agent can use its second `MCPToolset` for filesystem access to verify the file was created or to manage files in the output directory.
8.  **Response:** The agent confirms the video generation and provides the path to the final video file to the user.

-----

## Core Components

### 1\. `my_agent/agent.py` (The Agent)

This is the heart of the project. It defines the `root_agent` as an `LlmAgent` and equips it with:

  * **Model:** `LiteLlm(model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0")`.
  * **Instructions:** The `GOOGLE_THEMED_MANIM_VIDEO_GENERATOR` prompt from `google_prompt.py`.
  * **Tools:** Two `MCPToolset` instances:
    1.  One for the custom `manim_server.py` to handle video rendering.
    2.  One for the standard `@modelcontextprotocol/server-filesystem` to manage files.

### 2\. `my_agent/google_prompt.py` (The "Brain")

This is a comprehensive system prompt that acts as the creative director for the LLM. It contains strict rules and templates for:

  * **Mandatory Brand Colors:** `GOOGLE_BLUE`, `GOOGLE_RED`, etc..
  * **Design Philosophy:** Clean, minimal, and purposeful Material Design.
  * **Video Formats:** Configurations for 16:9 (horizontal) and 9:16 (vertical).
  * **Code Templates:** Reusable Python classes and functions for Google-style cards, bullet points, and transitions.
  * **Error Prevention:** A checklist of "Never Do" and "Always Do" to ensure high-quality, error-free output.

### 3\. `my_agent/manim_server.py` (The "Worker")

A lightweight `FastMCP` server that runs as a separate process to handle Manim operations securely and efficiently. It exposes two tools to the agent:

  * `execute_manim_code(manim_code: str)`: Takes Manim code as a string, saves it to `scene.py`, runs it via the Manim CLI, and stores the output in the `my_agent/media` directory.
  * `cleanup_manim_temp_dir(directory: str)`: A utility to remove temporary files.

### 4\. `my_agent/test_mcp.py` (The Tester)

A simple script to test the `manim_server.py` independently. It initializes a client session, connects to the server, and lists the available tools to confirm the server is running correctly.

## Setup and Usage

*(Inferred from project files)*

### Prerequisites

  * Python 3.10+
  * Google ADK
  * Manim
  * Node.js (for `npx`)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yash-kavaiya/google-adk-video-generator.git
    cd google-adk-video-generator
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    *(Note: A `requirements.txt` is not present, but based on imports, you will need at least)*

    ```bash
    pip install google-adk "mcp-client[stdio]" "mcp-server[fastmcp]" manim
    ```

4.  **Ensure MCP filesystem server is available:**
    The agent is configured to run the `npx` command directly.

### Running the Agent

This project is designed to be run using the Google ADK framework.

```bash
# Start the ADK server (which will manage the agent and its tools)
adk serve
```

You can then interact with the agent through the ADK's client interface or API.

### Running the Test Script

To verify that the `manim_server.py` is configured correctly, you can run its test script:

```bash
python my_agent/test_mcp.py
```

You should see output indicating the server initialized successfully and found the available tools.
