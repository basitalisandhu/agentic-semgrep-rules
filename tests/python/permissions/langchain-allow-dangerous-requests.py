from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper

# ruleid: langchain-allow-dangerous-requests
toolkit = RequestsToolkit(requests_wrapper=TextRequestsWrapper(headers={}), allow_dangerous_requests=True)
# ruleid: langchain-allow-dangerous-requests
tools = langchain_community.agent_toolkits.NLAToolkit.from_llm_and_url(llm, spec, allow_dangerous_requests=True)

# ok: langchain-allow-dangerous-requests
toolkit2 = RequestsToolkit(requests_wrapper=TextRequestsWrapper(headers={}), allow_dangerous_requests=False)
# ok: langchain-allow-dangerous-requests
toolkit3 = RequestsToolkit(requests_wrapper=TextRequestsWrapper(headers={}))
