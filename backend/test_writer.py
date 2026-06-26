from agents.writer_agent import WriterAgent

agent = WriterAgent()

article = {
    "title": "Google launches new Gemini AI model",
    "description": "Google announced a new Gemini model with improved reasoning capabilities."
}

result = agent.rewrite(article)

print(result)