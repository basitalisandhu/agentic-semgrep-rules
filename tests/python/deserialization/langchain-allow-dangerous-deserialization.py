from langchain_community.vectorstores import FAISS
from langchain.chains import load_chain

# ruleid: langchain-allow-dangerous-deserialization
store = FAISS.load_local("downloaded_index", embeddings, allow_dangerous_deserialization=True)
# ruleid: langchain-allow-dangerous-deserialization
chain = load_chain("chain.json", allow_dangerous_deserialization=True)

# ok: langchain-allow-dangerous-deserialization
store2 = FAISS.load_local("index", embeddings)
# ok: langchain-allow-dangerous-deserialization
store3 = FAISS.load_local("index", embeddings, allow_dangerous_deserialization=False)
