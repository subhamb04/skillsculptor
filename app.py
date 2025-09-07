import os
import gradio as gr
import asyncio
from agents import Runner, trace, gen_trace_id
from worker_agents.coordinator import coordinator

SHORT_TERM_TURNS = 4 
REPORT_PATH = "reports/gap_report.md"

def download_gap_report():
    if os.path.exists(REPORT_PATH) and os.path.getsize(REPORT_PATH) > 0:
        return REPORT_PATH
    return None

def init_session():
    for filename in os.listdir("reports"):
        file_path = os.path.join("reports", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return [], {"trace_id": gen_trace_id()}


async def chat_handler(message, history, memory_mode, memory_state, trace_state):
    if trace_state.get("trace_id") is None:
        trace_state["trace_id"] = gen_trace_id()

    trace_id = trace_state["trace_id"]

    with trace("SkillSculptor trace", trace_id=trace_id):
        if memory_mode == "Short-term":
            relevant_history = memory_state[-SHORT_TERM_TURNS:]
        else:
            relevant_history = memory_state

        conversation = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}" for m in relevant_history
        )
        conversation += f"\nUser: {message}"

        resp = await Runner.run(coordinator, f"Conversation so far:\n{conversation}")
        text = resp.final_output

        memory_state.append({"role": "user", "content": message})
        memory_state.append({"role": "assistant", "content": text})

        # Fake streaming back to user
        for i in range(1, len(text) + 1):
            await asyncio.sleep(0.02)
            yield text[:i]


with gr.Blocks() as demo:
    gr.Markdown("## 🤖 SkillSculptor Assistant")

    with gr.Row():
        memory_mode = gr.Radio(
            ["Long-term", "Short-term"],
            value="Short-term",
            label="Memory Mode"
        )

    memory_state = gr.State([])
    trace_state = gr.State({"trace_id": None})

    chat = gr.ChatInterface(
        fn=chat_handler,
        type="messages",  
        chatbot=gr.Chatbot(label="SkillSculptor Assistant", type="messages"),
        textbox=gr.Textbox(
            placeholder="Ask me about staffing, skills, or gaps...",
            container=True,
            scale=7
        ),
        title="Workforce Planning Chatbot",
        description="An agentic AI for staffing, skill gap analysis, and upskilling suggestions.",
        fill_height=True,
        additional_inputs=[memory_mode, memory_state, trace_state]
    )

    download_btn = gr.DownloadButton(
        "⬇️ Download Gap Report",
        value=download_gap_report,
        label="Download Gap Report",
        size='sm',
        variant='primary'
    )
    download_btn.click(fn=download_gap_report, outputs=download_btn)

    demo.load(init_session, inputs=None, outputs=[memory_state, trace_state])
    

if __name__ == "__main__":
    demo.launch(inbrowser=True)
