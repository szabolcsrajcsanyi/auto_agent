# streamlit_app.py
import uuid
import json
import streamlit as st
from code_editor import code_editor
from pydantic import BaseModel
from typing import Literal, List
from langgraph.types import Command
from collections import OrderedDict

from src.app.genai.agents.plan_and_execute.agent import plan_and_execute_agent
from src.app.genai.agents.plan_and_execute.schemas import ReviewPlan, PlanToReview, PlanExecute
from src.app.genai.agents.tool_manipulator.schemas import ReviewCode
from src.app.streamlit_app.schema import StreamOutput
from src.app.config.enums import AgentType, PlanReviewAction
from src.app.genai.shared.tool_manager import tool_manager


class ChatMessage(BaseModel):
    type: Literal["human", "ai"]
    content: List[str]
    node: Literal["planner", "decide_tool_use", "generate_tool", "answer", "retrieve_tools", "execute_step"] = None



if "messages" not in st.session_state:
    st.session_state.messages = OrderedDict()
if "stream_config" not in st.session_state:
    st.session_state.stream_config = {}
if "plan_review" not in st.session_state:
    st.session_state.plan_review = False
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

def render_planner(message: ChatMessage):
    if st.session_state.modify_plan:
        st.markdown("### ✏️ Modify the Plan")
        original_text = "\n".join(message.content)
        modified_plan = st.text_area("Edit the plan here:", value=original_text, height=200, key="modified_plan_text")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("💾 Save & Continue", use_container_width=True, key="save_con_btn"):
                st.session_state.plan_review = False
                st.session_state.modify_plan = False
                st.session_state.run_agent = True
                st.session_state.command_agent = Command(
                    resume=ReviewPlan(
                        action=PlanReviewAction.MODIFY,
                        steps=modified_plan.split("\n"),
                    )
                )
                st.rerun()
        with col2:
            if st.button("❌ Cancel Edit", use_container_width=True, key="cancel_edit_btn"):
                st.session_state.modify_plan = False
                st.rerun()
    
    else: 
        st.markdown("### 🧠 Planning...")
        st.markdown("Here's the plan I came up with:")
        st.markdown("#### ✅ Steps:")
        for i, step in enumerate(message.content, 1):
            st.markdown(f"- **Step {i}:** {step}")
            

        if st.session_state.give_feedback:
            st.markdown("### 💬 Give Feedback")
            feedback = st.text_area("Provide your feedback here:", height=100, key="feedback_text")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("💾 Send Feedback", use_container_width=True, key="send_feedback_btn"):
                    st.session_state.plan_review = False
                    st.session_state.give_feedback = False
                    st.session_state.run_agent = True
                    st.session_state.command_agent = Command(
                        resume=ReviewPlan(
                            action=PlanReviewAction.FEEDBACK,
                            feedback=feedback,
                        )
                    )
                    # del st.session_state.messages["planner"]
                    st.rerun()
            with col2:
                if st.button("❌ Cancel Feedback", use_container_width=True, key="cancel_feedback_btn"):
                    st.session_state.give_feedback = False
                    st.session_state.plan_review = True
                    st.rerun()

        if st.session_state.plan_review:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✅ Approve Plan", use_container_width=True, key="approve_plan_btn"):
                    st.session_state.plan_review = False
                    st.session_state.run_agent = True
                    st.session_state.command_agent = Command(
                        resume=ReviewPlan(
                            action=PlanReviewAction.APPROVE,
                        ))
                    st.rerun()

            with col2:
                if st.button("✏️ Modify Plan", use_container_width=True, key="modify_plan_btn"):
                    st.session_state.modify_plan = True
                    st.rerun()

            with col3:
                if st.button("💬 Give Feedback", use_container_width=True, key="feedback_btn"):
                    st.session_state.plan_review = False
                    st.session_state.give_feedback = True
                    st.rerun()
                
                

def render_decide_tool_use(message: ChatMessage):
    st.markdown(message.content[0])

def render_execute_step(message: ChatMessage):
    st.markdown(message.content[0])

def render_retrieve_tools(message: ChatMessage):
    st.markdown(message.content[0])

def render_generate_tool(message: ChatMessage):
    st.markdown(message.content[0])

def render_code_review(message: ChatMessage):
    if st.session_state.code_review:
        st.markdown("### 💬 Code Review")
        code = message.content[0]
        code_dict = code_editor(code=code, lang="python")

        if st.button("✅ Approve Code", use_container_width=True, key="approve_code_btn"):
            print(code_dict)



def render_messages():
    if len(st.session_state.messages) != 0:
        human_message: ChatMessage = st.session_state.messages.get("human")
        st.chat_message("human").markdown(human_message.content[0])

        with st.chat_message("ai"):
            for node, message in st.session_state.messages.items():
                    if node == "planner":
                        render_planner(message)
                    elif node == "decide_tool_use":
                        render_decide_tool_use(message)
                    elif node == "generate_tool":
                        render_generate_tool(message)
                    elif node == "retrieve_tools":
                        render_retrieve_tools(message)
                    elif node == "execute_step":
                        render_execute_step(message)
                    elif node == "code_review":
                        render_code_review(message)


def run_agent(user_input):
    print("AGENT RUNNING")
    st.session_state.run_agent = False

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
                st.session_state.messages["planner"] = chat_message
                render_planner(chat_message)

            elif output.human_plan_review:
                human_review: PlanToReview | ReviewCode = output.human_plan_review[0].value
                if isinstance(human_review, PlanToReview):
                    st.session_state.plan_review = True
                    st.rerun()
                elif isinstance(human_review, ReviewCode) and path != ():
                    chat_message.content.append(human_review.code)
                    st.session_state.messages["code_review"] = chat_message
                    st.session_state.code_review = True
                    render_code_review(chat_message)

            elif output.execute_step:
                chat_message.node = "execute_step"
                chat_message.content.append("### 🚀 Executing Step...")
                st.session_state.messages["execute_step"] = chat_message
                render_execute_step(chat_message)

            elif output.decide_tool_use:
                chat_message.node = "decide_tool_use"
                chat_message.content.append("### 🧠 Deciding tool use...")
                st.session_state.messages["decide_tool_use"] = chat_message
                render_decide_tool_use(chat_message)

            elif output.retrieve_tools:
                chat_message.node = "retrieve_tools"
                chat_message.content.append("### 🧭 Retrieving Tools...")
                st.session_state.messages["retrieve_tools"] = chat_message
                render_retrieve_tools(chat_message)

            elif output.generate_tool:
                chat_message.node = "generate_tool"
                chat_message.content.append("### 🛠️ Generating Tool...")
                st.session_state.messages["generate_tool"] = chat_message
                render_generate_tool(chat_message)




def main():
    with st.sidebar:
        st.title("Agent Configuration")
        agent_type = st.selectbox(
            "Select Agent Type",
            options=list(AgentType),
            format_func=lambda at: at.value.replace("_", " ").title()
        )

    render_messages()
    if st.session_state.run_agent:
        run_agent(st.session_state.command_agent)
    
    
    if user_input := st.chat_input("Enter your task..."):
        st.session_state.messages = OrderedDict()
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
