# Google-ADK-Video-Generator

## Architecture

This diagram illustrates the architecture of the Google ADK Video Generator agent.

```mermaid
graph TD
    subgraph "User"
        User_Input[User Prompt <br> e.g., "Create a reel..."]
    end

    subgraph "Google ADK Agent"
        A[LlmAgent <br> 'manim_video_generator_agent']
        LLM[LiteLlm <br> (Claude 3.5 Sonnet)]
        P[Prompt <br> (google_prompt.py)]

        User_Input --> A
        P --> A
        A -- uses --> LLM
        A -- uses --> T1[MCPToolset <br> (Manim)]
        A -- uses --> T2[MCPToolset <br> (Filesystem)]
    end

    subgraph "Manim Tool"
        T1 -- (stdio) --> S1[manim_server.py <br> (FastMCP)]
        S1 -- defines --> Tool_Exec[execute_manim_code]
        Tool_Exec -- runs --> Manim[MANIM_EXECUTABLE]
        Manim -- generates --> Video[Video File <br> (media/manim_tmp/...)]
    end

    subgraph "Filesystem Tool"
        T2 -- (stdio) --> S2[npx server-filesystem]
        S2 -- manages --> Files[Project Filesystem <br> (my_agent/)]
    end

    A -- "1. Generates Manim code" --> LLM
    LLM -- "2. Returns code" --> A
    A -- "3. Calls execute_manim_code" --> T1
    S1 -- "4. Executes code" --> Manim
    Manim -- "5. Creates video" --> Video
    S1 -- "6. Returns status" --> A
    A -- "7. (Optional) Manages files" --> T2
    S2 -- "8. (Optional) Accesses files" --> Files
    A -- "9. Returns result to user" --> User_Output[Agent Response]

    style A fill:#E8F0FE,stroke:#4285F4,stroke-width:2px
    style LLM fill:#E6F4EA,stroke:#34A853,stroke-width:2px
    style P fill:#FDF4E7,stroke:#FBBC04,stroke-width:2px
    style T1 fill:#FCE8E6,stroke:#EA4335,stroke-width:2px
    style S1 fill:#FCE8E6,stroke:#EA4335,stroke-width:2px
    style T2 fill:#FCE8E6,stroke:#EA4335,stroke-width:2px
    style S2 fill:#FCE8E6,stroke:#EA4335,stroke-width:2px
    style Video fill:#D2E3FC,stroke:#4285F4,stroke-width:1px
    style Files fill:#D2E3FC,stroke:#4285F4,stroke-width:1px
    style User_Input fill:#F1F3F4,stroke:#5F6368
    style User_Output fill:#F1F3F4,stroke:#5F6368
