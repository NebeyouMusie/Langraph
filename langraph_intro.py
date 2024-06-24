from typing import Annotated, Literal, TypedDict

from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from langgraph.checkpoint import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

import os
from dotenv import load_dotenv

load_dotenv()

# Define the tools for the agent to use
tools = [TavilySearchResults(max_results=1)]
tool_node = ToolNode(tools)

model = ChatGroq(temperature=0.5, api_key=os.getenv('GROQ_API_KEY'), model="mixtral-8x7b-32768")

# print(model.invoke('hello'))


# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to teh 'tools' node
    if last_message.tool_calls:
        return "tools"
    return END


# Define the function that calls the model
def call_model(state):
    messages = state['messages']
    response = model.invoke(messages)
    # We return a list, because this will get added to teh existing list
    return {"messages": [response]}

# Define a new Graph
workflow = StateGraph(MessagesState)

#Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Set the entrypoint as 'agent'
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use 'agent'.
    # This means there are the edges taken after the 'agent' node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
)

# We now add a normal edge from 'tools' to 'agent'.
# This means that after 'tools' is called, 'agent' node is called next.
workflow.add_edge("tools", "agent")

# Initialize memory to persist stte between graph runs
checkpointer = MemorySaver()

# Finally, we compile it!
# This compiles into a Langchain Runnable,
# meaning you can us it as you would any other runnable
# Note that we're (optionally) passing the memory when compiling the graph
app = workflow.compile(checkpointer=checkpointer)

# Use Runnable
final_state = app.invoke(
    {"messages": [HumanMessage(content='What is the weather in sf')]},
    config={"configurable": {"thread_id": 42}}
)

print(final_state["messages"][-1].content)