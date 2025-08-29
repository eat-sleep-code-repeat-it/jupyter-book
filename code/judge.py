import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from IPython.display import Markdown, display

"""
An agent is a self-contained unit that
    Has goals or tasks
    Has tools or capabilities (e.g., access to APIs, functions, reasoning)
    Makes decisions autonomously
    Can communicate with other agents or systems
 Agentic Design
    Tasks are complex or require reasoning steps
    Multiple tools or APIs need to be orchestrated
    You want traceability, modularity, and flexibility
Common Agentic Design Patterns
    Single Agent Tool-User
        An agent uses tools (functions, APIs) to solve a task autonomously
        RAG pipelines, assistants with function calling
    Planner–Executor
        One agent plans a task, another executes it step-by-step
        Task decomposition, multi-step reasoning
    Multi-Agent Collaboration
        Multiple specialized agents work together, possibly with a coordinator
        Research assistant with writer, researcher, editor
    Router or Dispatcher
        A system routes tasks to the appropriate agent/tool based on intent
        ool/agent selection, message routing
    Agent + Memory Loop
        Agent maintains short- or long-term memory across interactions
        Conversational agents, long-running workflows
    Graph-based Agent Flow (LangGraph)
        Agents connected as nodes in a graph that define logic flow
        Deterministic multi-step workflows with state
    Reflexion/Reflection Pattern
        Agent critiques its own outputs and retries
        Code generation, self-correcting agents
    Autonomous Agent Loop (AutoGPT style)
        Agent acts repeatedly toward a goal with planning, execution, memory, and feedback
        Full automation, research agents, long-term goals
Common Frameworks That Use Agentic Patterns
    LangGraph   Build stateful, multi-agent workflows using a graph model
    AutoGen     Multi-agent conversation orchestration with OpenAI models
    CrewAI      Teams of agents with roles and tools
    OpenAI Agents SDK   Tool-using LLM agents with structured protocols
Agentic Workflow
    User asks: “Summarize a PDF and email the summary.”
        Extract text from PDF
        Summarize
        Send email
    Agent 1 (Planner): Breaks it into sub-tasks:
    Agent 2: Calls PDF reader tool
    Agent 3: Uses LLM to summarize
    Agent 4: Sends email using SendGrid API
    Each agent can be isolated, reusable, and testable

"""
## Agentic Design
## Which pattern(s) did this use? Try updating this to add another Agentic design pattern
""" These kinds of patterns - to send a task to multiple models, and evaluate results,
are common where you need to improve the quality of your LLM response. This approach can be universally applied
to business projects where accuracy is critical.
"""            
load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set (and this is optional)")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")

if deepseek_api_key:
    print(f"DeepSeek API Key exists and begins {deepseek_api_key[:3]}")
else:
    print("DeepSeek API Key not set (and this is optional)")

if groq_api_key:
    print(f"Groq API Key exists and begins {groq_api_key[:4]}")
else:
    print("Groq API Key not set (and this is optional)")


request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaluate their intelligence. "
request += "Answer only with the question, no explanation."
messages = [{"role": "user", "content": request}]

openai = OpenAI()
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)
question = response.choices[0].message.content
print(question)


competitors = []
answers = []
messages = [{"role": "user", "content": question}]

# The API we know well

model_name = "gpt-4o-mini"

response = openai.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

# Anthropic has a slightly different API, and Max Tokens is required

model_name = "claude-3-7-sonnet-latest"

claude = Anthropic()
response = claude.messages.create(model=model_name, messages=messages, max_tokens=1000)
answer = response.content[0].text

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)


gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model_name = "gemini-2.0-flash"

response = gemini.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

deepseek = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com/v1")
model_name = "deepseek-chat"

response = deepseek.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

groq = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
model_name = "llama-3.3-70b-versatile"

response = groq.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

# It's nice to know how to use "zip"
for competitor, answer in zip(competitors, answers):
    print(f"Competitor: {competitor}\n\n{answer}")

# Let's bring this together - note the use of "enumerate"

together = ""
for index, answer in enumerate(answers):
    together += f"# Response from competitor {index+1}\n\n"
    together += answer + "\n\n"

## JUDGE
judge = f"""You are judging a competition between {len(competitors)} competitors.
Each model has been given this question:

{question}

Your job is to evaluate each response for clarity and strength of argument, and rank them in order of best to worst.
Respond with JSON, and only JSON, with the following format:
{{"results": ["best competitor number", "second best competitor number", "third best competitor number", ...]}}

Here are the responses from each competitor:

{together}

Now respond with the JSON with the ranked order of the competitors, nothing else. Do not include markdown formatting or code blocks."""

judge_messages = [{"role": "user", "content": judge}]

# Judgement time!

openai = OpenAI()
response = openai.chat.completions.create(
    model="o3-mini",
    messages=judge_messages,
)
results = response.choices[0].message.content
print(results)

# OK let's turn this into results!

results_dict = json.loads(results)
ranks = results_dict["results"]
for index, result in enumerate(ranks):
    competitor = competitors[int(result)-1]
    print(f"Rank {index+1}: {competitor}")


