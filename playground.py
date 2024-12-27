from phi.agent import Agent
from dotenv import load_dotenv
from phi.model.openai import OpenAIChat
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.playground import Playground, serve_playground_app
from phi.model.groq import Groq
from phi.playground.settings import PlaygroundSettings
import os

load_dotenv()

playground_settings = PlaygroundSettings(
    title="Veda's Playground",
    docs_enabled=False,
    cors_origin_list=["http://localhost", "http://127.0.0.1"],
)

web_agent = Agent(
    name="Web Agent",
    # model=OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    storage=SqlAgentStorage(table_name="web_agent", db_file="agents.db"),
    add_history_to_messages=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    # model=OpenAIChat(id="gpt-4o",api_key=os.getenv("OPENAI_API_KEY")),
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Use tables to display data"],
    storage=SqlAgentStorage(table_name="finance_agent", db_file="agents.db"),
    add_history_to_messages=True,
    markdown=True,
)

app = Playground(
    agents=[finance_agent, web_agent],
    settings=playground_settings,
).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)
