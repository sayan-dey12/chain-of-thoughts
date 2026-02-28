from openai import OpenAI
from dotenv import load_dotenv
import os 
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
    You are a helpful AI assistant in resolving user queries using chain of thought approach.
    You work on START , PLAN , OUTPUT steps.
    You need to first understand the problem and then PLAN what you need to do . The PLAN can be in multiple steps.
    Once you think enough PLAN was made , you can give an OUTPUT.
    
     Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).
    
    IMPORTANT EXECUTION RULES:
    - You MUST return ONLY ONE JSON object.
    - NEVER return an array.
    - NEVER return multiple steps.
    - After generating ONE step, STOP.
    - Wait for the next user/system message before continuing.
    - Do NOT predict future steps.
    - Do NOT generate OUTPUT unless explicitly asked to continue.

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }
    
     Example:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN": "content": "looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN": "content": "Yes, The BODMAS is correct thing to be done here" }
    PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10  = 1.5" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "step": "OUTPUT": "content": "3.5" }
    
"""
print("\n\n\n")

message_history = [
    {"role": "system" , "content": SYSTEM_PROMPT},
]

user_query=input("🐦‍🔥 Enter your query : ")

message_history.append({"role": "user", "content": user_query})

while(True):
    response = client.chat.completions.create(
        model="gemini-2.5-flash-lite",
        response_format={"type": "json_object"},
        messages=message_history
    )
        
    raw_content = response.choices[0].message.content
    message_history.append({"role":"assistant", "content": raw_content})
        
    parsed_content = json.loads(raw_content)
    # print("raw: ",raw_content)
    # print("parsed: ", parsed_content)
    # print(type(parsed_content))
    # print(type(raw_content))
    
    if parsed_content.get("step") == "START":
        print("👤 :" , parsed_content.get("content"))
        continue
    elif parsed_content.get("step") == "PLAN":
        print("🧠 :" , parsed_content.get("content"))
        continue
    elif parsed_content.get("step") == "Output":
        print("🤖 :" , parsed_content.get("content"))
        break
    
    message_history.append({
        "role": "user",
        "content": "Continue to next step. Follow rules strictly."
    })
    
print("\n\n\n")
    