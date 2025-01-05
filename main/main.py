from langchain import hub
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.tools import PythonAstREPLTool
import os
from langchain.agents import create_react_agent, AgentExecutor


load_dotenv()
# Set proxy configuration
proxy_url = "http://proxy-dmz.intel.com:912"
os.environ["HTTP_PROXY"] = proxy_url
os.environ["HTTPS_PROXY"] = proxy_url

def mainrun(question: str, chat_history: str):
    print("processing")
    tool = [PythonAstREPLTool()]
    instruction = """
        You are an agent designed to write a code to wanswer the question, 
        You have access to the python REPL, which you can use to execute python code, 
        if you got error, debug your code and try again.
        Only use the your final code as the final anwser to the question, 
        You might know the answer without running any code, but you still run the code to get the answer
        If it does not seem like you can write the code to answer the question, just return "i dont know" as the answer
    """
    base_prompt = hub.pull('langchain-ai/react-agent-template')
    #prompt = base_prompt.partial(instructions = instruction)
    llm = ChatOpenAI(temperature=0, model = 'gpt-4-turbo')
    agent = create_react_agent(llm = llm,tools=tool, prompt=base_prompt)
    agent_executor = AgentExecutor(agent= agent, tools= tool, verbose=True, handle_parsing_errors=True)
    
    res = agent_executor.invoke(input = {
        "input" : question,
        "instructions" : instruction,
        "chat_history" : chat_history
    })
    return res

if __name__ == "__main__":
    question = "write a code to multiply two numbers"
    print(mainrun(question=question, chat_history= ""))