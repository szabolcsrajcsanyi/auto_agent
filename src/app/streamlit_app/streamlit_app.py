import streamlit as st
from typing import Literal, List
from pydantic import BaseModel
from src.app.genai.agents.plan_and_execute.agent import plan_and_execute_agent
from src.app.genai.agents.tool_manipulator.schemas import BaseTaskState
from src.app.streamlit_app.schema import StreamOutput


class ChatMessage(BaseModel):
    type: Literal["user", "agent", "node"]
    content: str


def render_stream_event(label: str, state_dict: dict, key: str):
    st.markdown(label)
    with st.expander("🔍 View state", expanded=False):
        st.json(state_dict, expanded=False)


def main():
    st.title("🔁 Plan-and-Execute Agent")

    if "chat_log" not in st.session_state:
        st.session_state["chat_log"] = []

    if user_input := st.chat_input("Enter your task..."):
        # Log user message
        st.session_state["chat_log"].append(ChatMessage(type="user", content=user_input))
        st.chat_message("human").write(user_input)

        with st.chat_message("ai"):
            config = {
                "configurable": {"thread_id": "1"}
            }

            # Start stream
            for path, payload in plan_and_execute_agent.stream(
                input=BaseTaskState(task=user_input),
                config=config,
                stream_mode="updates",
                subgraphs=True
            ):
                output = StreamOutput(**payload)

                # Stream message depending on which step fired
                if output.planner:
                    st.session_state["chat_log"].append(ChatMessage(type="node", content="🧠 Planning..."))
                    render_stream_event("🧠 Planning...", output.planner.dict(), key="planner")

                elif output.decide_tool_use:
                    st.session_state["chat_log"].append(ChatMessage(type="node", content="🛠️ Deciding tool usage..."))
                    render_stream_event("🛠️ Deciding tool usage...", output.decide_tool_use.dict(), key="decide_tool_use")

                elif output.retrieve_tools:
                    st.session_state["chat_log"].append(ChatMessage(type="node", content="🔍 Retrieving tools..."))
                    render_stream_event("🔍 Retrieving tools...", output.retrieve_tools.dict(), key="retrieve_tools")

                elif output.generate_tool:
                    st.session_state["chat_log"].append(ChatMessage(type="node", content="🛠️ Tool generated."))
                    render_stream_event("🛠️ Tool Generated", output.generate_tool.dict(), key="generate_tool")

                    if "edited_tool_code" not in st.session_state:
                        st.session_state["edited_tool_code"] = output.generate_tool.tool_data.tool_output

                    code = st.text_area(
                        label="🔧 Modify tool code",
                        value=st.session_state["edited_tool_code"],
                        key="edited_tool_code_area",
                        height=300
                    )
                    if st.button("✅ Submit Modified Tool"):
                        st.session_state["edited_tool_code"] = code
                        st.success("Tool code submitted!")

                elif output.answer_without_tool:
                    st.session_state["chat_log"].append(ChatMessage(type="agent", content=output.answer_without_tool.answer))

                elif output.answer_with_tool:
                    st.session_state["chat_log"].append(ChatMessage(type="agent", content=output.answer_with_tool.answer))


if __name__ == "__main__":
    main()