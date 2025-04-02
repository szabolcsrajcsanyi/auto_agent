
from langchain_core.prompts import ChatPromptTemplate

from src.app.genai.agents.tool_manipulator.prompts import SYSTEM
from src.app.genai.shared.prompts import TOOL_SELECTOR_SYSTEM
from src.app.genai.shared.llm import llm
from src.app.genai.agents.tool_manipulator.schemas import ToolDecisionState


selector_prompt = ChatPromptTemplate.from_messages([
    ("system", TOOL_SELECTOR_SYSTEM),
    ("human", "{task}")
])


python_expert_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("human", "{user_input}")
])


tool_executor_agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that uses provided tools to directly perform tasks."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])


tool_selector_llm_chain = selector_prompt | llm.with_structured_output(ToolDecisionState)
python_expert_llm_chain = python_expert_template | llm

# if __name__ == "__main__":
#     task = "Turn on the lights in the kitchen"
#     user_input = HUMAN.format(task_description=task)
#     result = python_expert_llm_chain.invoke({
#         "user_input": user_input
#     })

#     result.pretty_print()
