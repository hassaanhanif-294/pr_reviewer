import asyncio
import gradio as gr
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_groq import ChatGroq
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
MCP_SCRIPT_PATH = str(BASE_DIR / "pr_analyzer.py")

server_params = StdioServerParameters(
    command="python",
    args=[MCP_SCRIPT_PATH],
)

async def run_agent_with_prompt(user_prompt):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            model = ChatGroq(
                model="llama-3.1-8b-instant",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
            agent = create_react_agent(model, tools)
            response = await agent.ainvoke({"messages": user_prompt})
            return str(response)

# Wrapper for Gradio to run async function
def sync_agent_response(prompt):
    return asyncio.run(run_agent_with_prompt(prompt))

# Gradio UI
with gr.Blocks(title="LangChain Agent UI") as demo:
    gr.Markdown("## 🤖 LangChain + MCP Agent Interface")
    user_input = gr.Textbox(label="Enter your prompt", placeholder="e.g., create a github repo called organicgoods")
    output = gr.Textbox(label="Agent Response")

    submit_btn = gr.Button("Run Agent")
    submit_btn.click(sync_agent_response, inputs=user_input, outputs=output)

demo.launch()
