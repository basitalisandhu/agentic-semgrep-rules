from agents import Agent, ShellTool

agent = Agent(
    name="Shell agent",
    tools=[
        # ok: langchain-dangerous-tools
        ShellTool(executor=ShellExecutor(), needs_approval=True),
    ],
)
