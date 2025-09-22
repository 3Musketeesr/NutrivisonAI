from langgraph_supervisor import create_supervisor 
from backend.llm import get_llm as sup_llm 
from backend.users.agent import get_user_agent
def get_supervisor(request, checkpointer=None):
    llm = sup_llm()
    user_agent = get_user_agent(request)

    supe = create_supervisor(
        agents=[user_agent],
        model = llm,
        prompt=(
            "You are a helpful assistant that helps users with food and diet. "
            "You manage a user agent and a search agent. Assign work to them appropriately."
        ),
    ).compile(checkpointer=checkpointer)
    return supe
