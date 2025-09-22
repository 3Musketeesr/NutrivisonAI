from langgraph.prebuilt import create_react_agent 
from backend.users.tools import get_user_tools
from backend.users.llm import get_llm 
from backend.users.prompts import get_user_prompt


def get_user_agent(request):
    model = get_llm()
    agent = create_react_agent(
        model=model,
        prompt=get_user_prompt(),
        tools=get_user_tools(request),
        name="use_agent"
        
    )
    return agent
