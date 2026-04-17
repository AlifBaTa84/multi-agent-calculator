from llm import llm

response = llm.invoke("Halo, berapa 2 + 2?")
print(response.content)