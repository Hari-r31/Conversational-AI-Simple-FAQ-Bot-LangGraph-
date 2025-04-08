from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver
from langgraph.graph.message import add_messages
import operator

# --- Step 1: Define FAQ data ---
faq_data = {
    "What is LangGraph?": "LangGraph is a library for building stateful, multi-agent applications with LLMs.",
    "How does LangGraph work?": "LangGraph works by defining state transitions in a graph using LangChain tools and custom logic.",
    "What is a state graph?": "A state graph defines how messages flow between nodes to maintain context and enable memory.",
    "Can I use LangGraph with OpenAI?": "Yes, LangGraph integrates seamlessly with OpenAI and other LLM providers.",
    "Is LangGraph open-source?": "Yes, LangGraph is an open-source project available on GitHub."
}

# --- Step 2: Create the core answer node ---
def answer_node(state):
    user_input = state["messages"][-1]["content"]
    response = faq_data.get(user_input, "Sorry, I don't know the answer to that question.")
    return {"messages": state["messages"] + [{"role": "assistant", "content": response}]}

# --- Step 3: Define the LangGraph state ---
def create_graph():
    builder = StateGraph({"messages": list})
    builder.add_node("answer", answer_node)
    builder.set_entry_point("answer")
    builder.set_finish_point("answer")
    return builder.compile()

# --- Step 4: Build and use the graph in a loop ---
if __name__ == "__main__":
    graph = create_graph()
    memory = MemorySaver()

    print("📘 FAQ Bot: Ask a question (type 'exit' to quit)\n")

    while True:
        user_question = input("You: ")
        if user_question.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break

        state = {"messages": [{"role": "user", "content": user_question}]}
        result = graph.invoke(state)

        bot_reply = result["messages"][-1]["content"]
        print(f"Bot: {bot_reply}\n")
