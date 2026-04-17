from llm import llm

response = llm.invoke("Buat script Python sederhana yang mencetak 'Hello, World!' ke konsol.")
print(response.content)