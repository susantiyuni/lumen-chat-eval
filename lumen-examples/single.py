from openai import OpenAI
from judges.lumen.correctness import FactualGradeJudge
import os

API_KEY = "sk-"
os.environ["OPENAI_API_KEY"] = API_KEY
os.environ["OPENAI_BASE_URL"] = "https://baseurl.llm/v1"

CHAT_MODEL = "alias-ha"
JUDGE_MODEL = "openai/meta-llama/Llama-3.3-70B-Instruct"

client = OpenAI()

user_input = "What's the capital of Japan?"
llm_output = "Tokyo"  # example response

# single judge
judge = FactualGradeJudge(model=JUDGE_MODEL)
judgment = judge.judge(input=user_input, output=llm_output)
print("Score (1-5):", judgment.score)
print("Reasoning:", judgment.reasoning)
