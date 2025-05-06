import streamlit as st
from langgraph.types import Command
from streamlit_monaco import st_monaco

from app.streamlit_app.schema import ChatMessage
from app.config.enums import PlanReviewAction, CodeReviewAction, PlanReviewType
from app.genai.agents.plan_and_execute.schemas import ReviewPlan
from app.genai.agents.tool_manipulator.schemas import ReviewCode


def render_plan_common(message: ChatMessage, replanner: bool = False):
    if replanner:
        plan_type = "replan"
        title = "Replanning"
    else:
        plan_type = "plan"
        title = "Planning"

    st.markdown(f"### 🧠 {title}...")
    st.json(message.state.model_dump(), expanded=False)

    if replanner and hasattr(message, "past_steps"):
        st.markdown("#### 📑 Previous Steps:")
        for i, (task, answer) in enumerate(message.past_steps, 1):
            with st.expander(f"**Step {i}:** {task[:60]}..."):
                st.markdown(f"**Task:** {task}")
                st.markdown(f"**Answer:** {answer}")

    if st.session_state.modify_plan:
        st.markdown("### ✏️ Modify the Plan")
        original_text = "\n".join(message.content)
        modified_plan = st.text_area("Edit the plan here:", value=original_text, height=200, key=f"{plan_type}_modified_plan_text")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("💾 Save & Continue", use_container_width=True, key=f"{plan_type}_save_con_btn"):
                # st.session_state.plan_review = False
                st.session_state.plan_options = False
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
            if st.button("❌ Cancel Edit", use_container_width=True, key=f"{plan_type}_cancel_edit_btn"):
                st.session_state.modify_plan = False
                st.rerun()

    elif st.session_state.plan_review:
        st.markdown("Here's the plan I came up with:")
        st.markdown("#### ✅ Steps:")
        for i, step in enumerate(message.content, 1):
            st.markdown(f"- **Step {i}:** {step}")

        if st.session_state.give_feedback:
            st.markdown("### 💬 Give Feedback")
            feedback = st.text_area("Provide your feedback here:", height=100, key=f"{plan_type}_feedback_text")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("💾 Send Feedback", use_container_width=True, key=f"{plan_type}_send_feedback_btn"):
                    st.session_state.plan_options = False
                    st.session_state.give_feedback = False
                    st.session_state.run_agent = True
                    st.session_state.command_agent = Command(
                        resume=ReviewPlan(
                            action=PlanReviewAction.FEEDBACK,
                            feedback=feedback,
                        )
                    )
                    st.rerun()
            with col2:
                if st.button("❌ Cancel Feedback", use_container_width=True, key=f"{plan_type}_cancel_feedback_btn"):
                    st.session_state.give_feedback = False
                    st.session_state.plan_options = True
                    st.rerun()

        elif st.session_state.plan_options:
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ Approve Plan", use_container_width=True, key=f"{plan_type}_approve_plan_btn"):
                    # st.session_state.plan_review = False
                    st.session_state.plan_options = False
                    st.session_state.run_agent = True
                    st.session_state.command_agent = Command(
                        resume=ReviewPlan(
                            action=PlanReviewAction.APPROVE
                        ))
                    print("PRESSED APPROVE")
                    st.rerun()
            with col2:
                if st.button("✏️ Modify Plan", use_container_width=True, key=f"{plan_type}_modify_plan_btn"):
                    st.session_state.modify_plan = True
                    st.rerun()
            with col3:
                if st.button("💬 Give Feedback", use_container_width=True, key=f"{plan_type}_feedback_btn"):
                    st.session_state.plan_options = False
                    st.session_state.give_feedback = True
                    st.rerun()
                

def render_planner(message: ChatMessage):
    render_plan_common(message, replanner=False)


def render_replanner(message: ChatMessage):
    render_plan_common(message, replanner=True)

                
def render_decide_tool_use(message: ChatMessage):
    st.markdown(message.content[0])
    st.json(message.state.model_dump(), expanded=False)


def render_execute_step(message: ChatMessage):
    st.markdown(message.content[0])
    st.json(message.state.model_dump(), expanded=False)


def render_retrieve_tools(message: ChatMessage):
    st.markdown(message.content[0])
    st.json(message.state.model_dump(), expanded=False)


def render_decide_candidate_tool(message: ChatMessage):
    st.markdown(message.content[0])
    st.json(message.state.model_dump(), expanded=False)


def render_generate_tool(message: ChatMessage):
    st.markdown(message.content[0])
    st.json(message.state.model_dump(), expanded=False)


def render_code_review(message: ChatMessage):
    st.json(message.state.model_dump(), expanded=False)
    if st.session_state.code_review:
        st.markdown("### 💬 Code Review")
        code = message.content[0]
        content = st_monaco(value=code, height="500px", language="python", theme="vs-dark")
        
        if st.session_state.code_give_feedback:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("✅ Approve Code", use_container_width=True):
                    st.session_state.code_review = False
                    st.session_state.run_agent = True
                    st.session_state.command_agent = Command(
                        resume=ReviewCode(
                            code=content,
                            action=CodeReviewAction.APPROVE,
                        ))
                    st.rerun()

            with col2:
                if st.button("💬 Give Feedback", use_container_width=True):
                    st.session_state.code_give_feedback = False
                    st.rerun()
        else:
            st.markdown("### 💬 Give Feedback")
            feedback = st.text_area("Provide your feedback here:", height=100)
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("💾 Send Feedback", use_container_width=True):
                    pass
                    st.session_state.code_give_feedback = True
                    st.session_state.run_agent = True
                    st.session_state.command_agent = Command(
                        resume=ReviewCode(
                            code=content,
                            action=CodeReviewAction.FEEDBACK,
                            feedback=feedback,
                        )
                    )
                    del st.session_state.messages["code_review"]
                    st.rerun()
            with col2:
                if st.button("❌ Cancel Feedback", use_container_width=True):
                    st.session_state.code_give_feedback = True
                    st.rerun()


def render_answer_with_tool(message: ChatMessage):
    st.markdown(message.content[0])
    st.json(message.state.model_dump(), expanded=False)


def render_answer_without_tool(message: ChatMessage):
    st.markdown(message.content[0])
    st.json(message.state.model_dump(), expanded=False)


def render_final_answer(message: ChatMessage):
    st.markdown(message.content[0])
    st.json(message.state.model_dump(), expanded=False)
    st.write(message.state.response)

def render_evaluate_tool_outcome(message: ChatMessage):
    st.markdown(message.content[0])
    st.json(message.state.model_dump(), expanded=False)


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
                elif node == "decide_candidate_tool":
                    render_decide_candidate_tool(message)
                elif node == "execute_step":
                    render_execute_step(message)
                elif node == "code_review":
                    render_code_review(message)
                elif node == "answer_with_tool":
                    render_answer_with_tool(message)
                elif node == "answer_without_tool":
                    render_answer_without_tool(message)
                elif node == "evaluate_tool_outcome":
                    render_evaluate_tool_outcome(message)
                elif node == "replanner":
                    render_replanner(message)
                elif node == "final_answer":
                    render_final_answer(message)
