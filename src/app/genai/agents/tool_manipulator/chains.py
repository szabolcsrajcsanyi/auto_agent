
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.genai.llm import llm, tool_generate_llm
from app.genai.agents.tool_manipulator.schemas import (
    ToolDecisionState, 
    CandidateTool,
    EvaluationResult
)
from app.config.enums import AgentType
from app.config.registry import COMMON_PROMPT_CONFIG


def determin_possible_tool_chain() -> RunnablePassthrough:
    selector_prompt = ChatPromptTemplate.from_messages([
        ("system", COMMON_PROMPT_CONFIG["possible_tool"]["system_prompt"]),
        ("human", COMMON_PROMPT_CONFIG["possible_tool"]["human_prompt"]),
    ])
    return selector_prompt | llm.with_structured_output(ToolDecisionState)


def python_expert_chain() -> RunnablePassthrough:
    expert_prompt = ChatPromptTemplate.from_messages([
        ("system", COMMON_PROMPT_CONFIG["python_expert"]["system_prompt"]),
        ("human", COMMON_PROMPT_CONFIG["python_expert"]["human_prompt"]),
    ])
    return expert_prompt | tool_generate_llm


def candidate_picker_chain() -> RunnablePassthrough:
    tool_selector_prompt = ChatPromptTemplate.from_messages([
        ("system", COMMON_PROMPT_CONFIG["candidate_picker_chain"]["system_prompt"]),
        ("human", COMMON_PROMPT_CONFIG["candidate_picker_chain"]["human_prompt"]),
    ])
    return tool_selector_prompt | llm.with_structured_output(CandidateTool)


def tool_evaluator_chain() -> RunnablePassthrough: 
    tool_eval_prompt = ChatPromptTemplate.from_messages([
        ("system", COMMON_PROMPT_CONFIG["tool_evaluator"]["system_prompt"]),
        ("human", COMMON_PROMPT_CONFIG["tool_evaluator"]["human_prompt"]),
    ]) 
    return tool_eval_prompt | llm.with_structured_output(EvaluationResult)


#TODO:
# tool_executor_agent_prompt = ChatPromptTemplate.from_messages([
#     ("system", COMMON_PROMPT_CONFIG["tool_executor_agent_prompt"]["system_prompt"]),
#     ("human", "{input}"),
#     ("placeholder", "{agent_scratchpad}")
# ])


# if __name__ == "__main__":
#     task = "Turn on the lights in the kitchen"
#     user_input = HUMAN.format(task_description=task)
#     result = python_expert_llm_chain.invoke({
#         "user_input": user_input
#     })

#     result.pretty_print()
