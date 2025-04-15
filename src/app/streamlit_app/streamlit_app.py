# streamlit_app.py
import uuid
import streamlit as st

from collections import OrderedDict

from src.app.config.enums import AgentType, PlanReviewType
from src.app.genai.tools.tool_manager import tool_manager
from src.app.genai.agents.plan_and_execute.agent import plan_and_execute_agent
from src.app.genai.agents.plan_and_execute.schemas import PlanToReview, PlanExecute
from src.app.genai.agents.tool_manipulator.schemas import ReviewCode
from src.app.streamlit_app.schema import ChatMessage, StreamOutput
from src.app.streamlit_app.renders import (
    render_messages,
    render_planner,
    render_replanner,
    render_execute_step,
    render_decide_tool_use,
    render_retrieve_tools,
    render_decide_candidate_tool,
    render_generate_tool,
    render_code_review,
    render_answer_with_tool,
    render_answer_without_tool,
    render_final_answer
)


if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
if "messages" not in st.session_state:
    st.session_state.messages = OrderedDict()
if "stream_config" not in st.session_state:
    st.session_state.stream_config = {}
if "plan_review" not in st.session_state:
    st.session_state.plan_review = True
if "plan_options" not in st.session_state:
    st.session_state.plan_options = False
if "run_agent" not in st.session_state:
    st.session_state.run_agent = False
if "command_agent" not in st.session_state:
    st.session_state.command_agent = None
if "modify_plan" not in st.session_state:
    st.session_state.modify_plan = False
if "give_feedback" not in st.session_state:
    st.session_state.give_feedback = False
if "code_review" not in st.session_state:
    st.session_state.code_review = False
if "code_edit" not in st.session_state:
    st.session_state.code_edit = ""
if "code_give_feedback" not in st.session_state:
    st.session_state.code_give_feedback = True


def run_agent(user_input):
    print("AGENT RUNNING")
    st.session_state.run_agent = False
    print(user_input)

    with st.chat_message("ai"):
        for path, payload in plan_and_execute_agent.stream(
            input=user_input,
            config=st.session_state["stream_config"],
            stream_mode="updates",
            subgraphs=True
        ):
            output = StreamOutput(**payload)
            chat_message = ChatMessage(type="ai", content=[])
            if output.planner:
                chat_message.node = "planner"
                for step in output.planner.plan.steps:
                    chat_message.content.append(step)
                chat_message.state = output.planner
                st.session_state.messages["planner"] = chat_message
                render_planner(chat_message)

            elif output.human_plan_review:
                human_review: PlanToReview | ReviewCode = output.human_plan_review[0].value
                chat_message.state = human_review
                if isinstance(human_review, PlanToReview):
                    st.session_state.plan_options = True
                    st.rerun()
                elif isinstance(human_review, ReviewCode) and path != ():
                    chat_message.content.append(human_review.code)
                    st.session_state.messages["code_review"] = chat_message
                    st.session_state.code_review = True
                    render_code_review(chat_message)

            elif output.execute_step:
                chat_message.node = "execute_step"
                chat_message.content.append("### 🚀 Executing Step...")
                chat_message.state = output.execute_step
                st.session_state.messages["execute_step"] = chat_message
                render_execute_step(chat_message)

            elif output.decide_tool_use:
                chat_message.node = "decide_tool_use"
                chat_message.content.append("### 🧠 Deciding tool use...")
                chat_message.state = output.decide_tool_use
                st.session_state.messages["decide_tool_use"] = chat_message
                render_decide_tool_use(chat_message)

            elif output.retrieve_tools:
                chat_message.node = "retrieve_tools"
                chat_message.content.append("### 🧭 Retrieving Tools...")
                chat_message.state = output.retrieve_tools
                st.session_state.messages["retrieve_tools"] = chat_message
                
                render_retrieve_tools(chat_message)

            elif output.generate_tool:
                chat_message.node = "generate_tool"
                chat_message.content.append("### 🛠️ Generating Tool...")
                chat_message.state = output.generate_tool
                st.session_state.messages["generate_tool"] = chat_message
                render_generate_tool(chat_message)

            elif output.answer_with_tool:
                chat_message.node = "answer_with_tool"
                chat_message.content.append("### 🤖 Answering with Tool...")
                chat_message.state = output.answer_with_tool
                st.session_state.messages["answer_with_tool"] = chat_message
                render_answer_with_tool(chat_message)

            elif output.answer_without_tool:
                chat_message.node = "answer_without_tool"
                chat_message.content.append("### 🤖 Answering without Tool...")
                chat_message.state = output.answer_without_tool
                st.session_state.messages["answer_without_tool"] = chat_message
                render_answer_without_tool(chat_message)

            elif output.replanner:
                chat_message.node = "replanner"
                for step in output.replanner.plan.steps:
                    chat_message.content.append(step)
                chat_message.past_steps = []
                for step in output.replanner.past_steps:
                    chat_message.past_steps.append(step)
                chat_message.state = output.replanner
                st.session_state.messages["replanner"] = chat_message
                render_replanner(chat_message)

            elif output.final_answer:
                chat_message.node = "final_answer"
                chat_message.content.append("## ✅ Final Answer")
                chat_message.state = output.final_answer
                st.session_state.messages["final_answer"] = chat_message
                render_final_answer(chat_message)

            elif output.decide_candidate_tool:
                chat_message.node = "decide_candidate_tool"
                chat_message.content.append("### 🧠 Deciding Candidate Tool...")
                chat_message.state = output.decide_candidate_tool
                st.session_state.messages["decide_candidate_tool"] = chat_message
                render_decide_candidate_tool(chat_message)

            elif output.plan_with_feedback:
                for step in output.plan_with_feedback.plan.steps:
                    chat_message.content.append(step)
                chat_message.state = output.plan_with_feedback

                if output.plan_with_feedback.feedback_type == PlanReviewType.PLAN:
                    chat_message.node = "planner"
                    st.session_state.messages["planner"] = chat_message
                else:
                    chat_message.past_steps = []
                    for step in output.plan_with_feedback.past_steps:
                        chat_message.past_steps.append(step)
                    chat_message.node = "replanner"
                    st.session_state.messages["replanner"] = chat_message


def main():
    with st.sidebar:
        if st.button("🔄 New Task", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key not in {"agent_type"}:  # Keep agent type if you want
                    del st.session_state[key]
            st.rerun()
        st.title("Agent Configuration")
        agent_type = st.selectbox(
            "Select Agent Type",
            options=list(AgentType),
            format_func=lambda at: at.value.replace("_", " ").title()
        )


    render_messages()
    if st.session_state.run_agent:
        run_agent(st.session_state.command_agent)
    
    if not st.session_state.chat_started:
        if user_input := st.chat_input("Enter your task..."):
            st.session_state.chat_started = True
            st.session_state.messages = OrderedDict()
            # st.rerun()
            render_messages()
            st.session_state.messages["human"] = ChatMessage(type="human", content=[user_input])
            st.chat_message("human").write(user_input)
            st.session_state["stream_config"] = {
                "configurable": {
                    "thread_id": str(uuid.uuid4()),
                    "agent_type": agent_type,
                    "tool_manager": tool_manager
                }
            }
            run_agent(PlanExecute(task=user_input))    


if __name__ == "__main__":
    main()
