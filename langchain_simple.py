import os
import httpx
import urllib3
import langchain
print(f"LangChain version: {langchain.__version__}")

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI as LangchainChatOpenAI
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def create_client_with_ssl_config():
    return httpx.Client(verify=False)

load_dotenv()
if not os.path.exists(".env"):
    raise FileNotFoundError("No .env file found. Please create one with your environment variables.")
else:
    print(".env file found and loaded.")

client = create_client_with_ssl_config()
model = LangchainChatOpenAI(
    model_name="gpt-3.5-turbo",
    # Uncomment ONE of the following:
    # openai_api_key=getpass.getpass("Enter your OpenAI API key: "),
    http_client=client,
    temperature=0.7,
)

result = model.invoke("Hello, my name is") 
print(f"Langchain Result: {result}")
