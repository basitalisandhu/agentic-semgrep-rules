from langchain_experimental.agents import create_pandas_dataframe_agent, create_csv_agent

# ruleid: langchain-allow-dangerous-code
agent = create_pandas_dataframe_agent(llm, df, allow_dangerous_code=True)
# ruleid: langchain-allow-dangerous-code
csv_agent = create_csv_agent(llm, "data.csv", verbose=True, allow_dangerous_code=True)
# ruleid: langchain-allow-dangerous-code
toolkit = langchain_experimental.agents.create_spark_dataframe_agent(llm, df, allow_dangerous_code=True)

# ok: langchain-allow-dangerous-code
safe = create_pandas_dataframe_agent(llm, df, allow_dangerous_code=False)
# ok: langchain-allow-dangerous-code
plain = create_pandas_dataframe_agent(llm, df)
