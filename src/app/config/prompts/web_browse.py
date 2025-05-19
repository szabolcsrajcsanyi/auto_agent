WEB_BROWSE_PLAN_SYSTEM_PROMPT = """\
For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps. \
"""

WEB_BROWSE_REPLANNER_SYSTEM_PROMPT = """\
For the given objective, revise the current plan with a minimal and efficient step-by-step list. \
Only include steps that still need to be completed, and remove any that are already done. \
Each step should be clear, specific, and self-contained, requiring no external assumptions. \
Do not add unnecessary steps. If the objective has already been fully achieved, clearly state that no further actions are required.
"""

WEB_BROWSE_REPLANNER_HUMAN_PROMPT = """\
You previously created a plan to accomplish the following task:
{task}

Your original plan was:
{plan}

You've successfully completed these steps:
{past_steps}

Considering the completed steps, update your remaining plan clearly and succinctly. \
If no further steps are needed and the task is complete, explicitly state this. \
Only include tasks still necessary to fully achieve the user's request. \
"""
