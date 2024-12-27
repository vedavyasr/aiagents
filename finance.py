from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

load_dotenv()

web_agent = Agent(
    name="Web Agent",
    # model=Groq(id="llama-3.3-70b-versatile"),
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],
    show_tool_calls=True,
    markdown=True,
    instructions=["Always include sources"],
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    # model=OpenAIChat(id="gpt-4o"),
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True,analyst_recommendations=True,stock_fundamentals=True)],
    show_tool_calls=True,
    markdown=True,
    instructions=["Use tables to display"],
    debug_mode=True
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    # model=OpenAIChat(id="gpt-4o"),
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["always include sources", "use tables to display"],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("Summarize analyst recommendations for TSLA", steam=True)