from src.app.genai.agents.tool_manipulator.schemas import BaseTaskState
from src.app.genai.agents.plan_and_execute.agent import plan_and_execute_agent


def main():
    # Example input task
    task = "Buy a milk in the grocery store"

    # Initial input state
    initial_state = BaseTaskState(task=task)

    # Invoke the LangGraph graph
    # result = graph.invoke(initial_state)


    for output in plan_and_execute_agent.stream(initial_state, stream_mode="updates"):
        print(output)

    # Print the final answer state
    # print(f"Task: {result['task']}")
    # print(f"Answer: {result['answer']}")

if __name__ == "__main__":
    main()


