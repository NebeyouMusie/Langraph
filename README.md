# Langraph
 -  In this repo is an introduction to Langraph.[LangGraph](https://langchain-ai.github.io/langgraph/) is a library for building stateful, multi-actor applications with LLMs, used to create agent and multi-agent workflows.

## Description
 - One of the central concepts of LangGraph is state. Each graph execution creates a state that is passed between nodes in the graph as they execute, and each node updates this internal state with its return value after it executes. The way that the graph updates its internal state is defined by either the type of graph chosen or a custom function.
 - In this project I have used a simple example that Langraph provided.It's an agent that can search the web using [Tavily Search API](https://tavily.com/).

## Step-by-step Breakdown
1. **Initialize the model and tools.**
 - we use Chat as our LLM. NOTE: we need make sure the model knows that it has these tools available to call. We can do this by converting the LangChain tools into the format for OpenAI tool calling using the `.bind_tools()` method.
 - we define the tools we want to use - a web search tool in our case.

2. **Initialize graph with state.**
 - we initialize graph (`StateGraph`) by passing state schema (in our case `MessagesState`)
 - `MessagesState` is a prebuilt state schema that has one attribute -- a list of LangChain Message objects, as well as logic for merging the updates from each node into the state.

3. **Define graph nodes.**
 - There are two main nodes we need:
    - The `agent` node: responsible for deciding what (if any) actions to take.
    - The `tools` node that invokes tools: if the agent decides to take an action, this node will then execute that action.

4. **Define entry point and graph edges.**
 - First, we need to set the entry point for graph execution - `agent` node.
 - Then we define one normal and one conditional edge. Conditional edge means that the destination depends on the contents of the graph's state (`MessageState`). In our case, the destination is not known until the agent (LLM) decides.

 - Conditional edge: after the agent is called, we should either:
    a. Run tools if the agent said to take an action, OR
    b. Finish (respond to the user) if the agent did not ask to run tools
 - Normal edge: after the tools are invoked, the graph should always return to the agent to decide what to do next

5. **Compile the graph.**
 - When we compile the graph, we turn it into a LangChain Runnable, which automatically enables calling `.invoke()`, `.stream()` and `.batch()` with your inputs
 - We can also optionally pass checkpointer object for persisting state between graph runs, and enabling memory, human-in-the-loop workflows, time travel and more. In our case we use `MemorySaver` - a simple in-memory checkpointer

6. **Execute the graph.**
 a. LangGraph adds the input message to the internal state, then passes the state to the entrypoint node, "agent".
 b. The "agent" node executes, invoking the chat model.
 c. The chat model returns an AIMessage. LangGraph adds this to the state.
 d. Graph cycles the following steps until there are no more tool_calls on AIMessage:
  - If AIMessage has tool_calls, "tools" node executes
  - The "agent" node executes again and returns AIMessage
 e. Execution progresses to the special END value and outputs the final state. And as a result, we get a list of all our chat messages as output.

## Libraries Used
 - langchain-community==0.2.5
 - langchain-core==0.2.9
 - langchain-groq==0.1.5
 - langgraph==0.1.1
 - python-dotenv==1.0.1

## Installation
 1. Prerequisites
    - Git
    - Command line familiarity
 2. Clone the Repository: `git clone https://github.com/NebeyouMusie/Langraph.git`
 3. Create and Activate Virtual Environment (Recommended)
    - `python -m venv venv`
    - `source venv/bin/activate` or `venv/bin/activate` for windows
 4. Navigate to the project's directory `cd ./Langraph` using your terminal
 5. Install Libraries: `pip install -r requirements.txt`
 6. run `python langraph_intro.py`

## Collaboration
- Collaborations are welcomed ❤️
   
## Contact
 - LinkedIn: [Nebeyou Musie](https://www.linkedin.com/in/nebeyou-musie)
 - Gmail: nebeyoumusie@gmail.com
 - Telegram: [Nebeyou Musie](https://t.me/NebeyouMusie)




