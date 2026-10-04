from langchain.agents import load_tools
from langchain_community.tools import ShellTool
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.utilities import PythonREPL

# ruleid: langchain-dangerous-tools
shell = ShellTool()
# ruleid: langchain-dangerous-tools
repl = PythonREPLTool()
# ruleid: langchain-dangerous-tools
tools = load_tools(["terminal", "wikipedia"], llm=llm)
# ruleid: langchain-dangerous-tools
raw = PythonREPL()


def build_agent(llm):
    # ruleid: langchain-dangerous-tools
    return initialize_agent([langchain_community.tools.ShellTool()], llm)


# ok: langchain-dangerous-tools
safe_tools = load_tools(["wikipedia", "arxiv"], llm=llm)
# ok: langchain-dangerous-tools
search = DuckDuckGoSearchRun()
# ok: langchain-dangerous-tools
calculator = Calculator()
