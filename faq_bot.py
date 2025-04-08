from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import List, Dict

# Step 1: FAQ data
faq_data = {
    "What is LangGraph?": "LangGraph is a library for building stateful, multi-agent applications with LLMs.",
    "How does LangGraph work?": "LangGraph works by defining state transitions in a graph using LangChain tools and custom logic.",
    "What is a state graph?": "A state graph defines how messages flow between nodes to maintain context and enable memory.",
    "Can I use LangGraph with OpenAI?": "Yes, LangGraph integrates seamlessly with OpenAI and other LLM providers.",
    "Is LangGraph open-source?": "Yes, LangGraph is an open-source project available on GitHub."
}

# Step 2: Define state schema using Pydantic
class ChatState(BaseModel):
    messages: List[Dict[str, str]]

# Step 3: Answer logic
def answer_node(state: ChatState) -> ChatState:
    last_msg = state.messages[-1]["content"]
    reply = faq_data.get(last_msg, "Sorry, I don't know the answer to that.")
    state.messages.append({"role": "bot", "content": reply})
    return state

# Step 4: Define graph flow
def create_graph():
    builder = StateGraph(ChatState)  # FIX: use Pydantic class instead of dict
    builder.add_node("answer", answer_node)
    builder.set_entry_point("answer")
    builder.set_finish_point("answer")
    return builder.compile()

# Step 5: Run CLI loop
if __name__ == "__main__":
    graph = create_graph()

    print("📘 FAQ Bot: Ask a question (type 'exit' to quit)\n")

    while True:
        user_question = input("You: ")
        if user_question.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break

        state = ChatState(messages=[{"role": "user", "content": user_question}])
        result = graph.invoke(state)

        bot_reply = result["messages"][-1]["content"]
        print(f"Bot: {bot_reply}\n")

