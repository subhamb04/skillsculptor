# app.py
import gradio as gr
import asyncio
from agents import Runner, trace, gen_trace_id
from worker_agents.coordinator import coordinator

# --- Config ---
SHORT_TERM_TURNS = 4  # how many turns to remember in short-term

# --- Chat handler with memory toggle ---
async def chat_handler(message, history, memory_mode):
    """
    message: str (latest user message)
    history: list of {"role": "user"/"assistant", "content": "..."} dicts
    memory_mode: "Long-term" or "Short-term"
    """
    trace_id = gen_trace_id()
    with trace("SkillSculptor trace", trace_id=trace_id):
        if memory_mode == "Short-term":
            relevant_history = history[-SHORT_TERM_TURNS:]
        else:
            relevant_history = history

        # Build transcript
        conversation = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}" for m in relevant_history
        )
        conversation += f"\nUser: {message}"

        # Run coordinator agent
        resp = await Runner.run(coordinator, f"Conversation so far:\n{conversation}")
        text = resp.final_output

        # Fake streaming back to user
        for i in range(1, len(text) + 1):
            await asyncio.sleep(0.02)
            yield text[:i]

# --- Gradio UI ---
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 SkillSculptor Assistant")

    with gr.Row():
        memory_mode = gr.Radio(
            ["Long-term", "Short-term"],
            value="Short-term",
            label="Memory Mode"
        )

    chat = gr.ChatInterface(
        fn=chat_handler,
        type="messages",  # role/content format
        chatbot=gr.Chatbot(label="SkillSculptor Assistant", type="messages"),
        textbox=gr.Textbox(
            placeholder="Ask me about staffing, skills, or gaps...",
            container=True,
            scale=7
        ),
        title="Workforce Planning Chatbot",
        description="An agentic AI for staffing, skill gap analysis, and upskilling suggestions.",
        fill_height=True,
        additional_inputs=[memory_mode]
    )

if __name__ == "__main__":
    demo.launch(inbrowser=True)
