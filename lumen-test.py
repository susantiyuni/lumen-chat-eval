import json
from judges.lumen.correctness import FactualGradeJudge
import os

API_KEY = "sk-"
os.environ["OPENAI_API_KEY"] = API_KEY
os.environ["OPENAI_BASE_URL"] = "https://baseurl.llm/v1"

JUDGE_MODEL1 = "openai/meta-llama/Llama-3.3-70B-Instruct"
JUDGE_MODEL2 = "openai/alias-ha"
max_chars = 2000

judges = [
    FactualGradeJudge(model=JUDGE_MODEL1),
    FactualGradeJudge(model=JUDGE_MODEL2),
]

# GoTriple chat logs
with open("logs/exports1770993570423-lf-traces-export-cmfnrnig0000ht607n1wls6sl.jsonl", "r") as f:
    logs = [json.loads(line) for line in f]

for i, log in enumerate(logs[:2]):
# for i, log in enumerate(logs):
    user_input = log.get("input")
    llm_output = log.get("output")
    llm_output = llm_output[:max_chars]
    print (i, user_input)
    # print (llm_output)

    if not user_input or not llm_output:
        continue  # skip incomplete entries

    judgments = [j.judge(user_input, llm_output) for j in judges]

    # Aggregate scores
    avg_score = sum(j.score for j in judgments) / len(judgments)

    print(f"Log ID: {log.get('id')}")
    for i, j_res in enumerate(judgments, start=1):
        print(f"  Judge {i} score: {j_res.score}")
        print(f"  Judge {i} reasoning: {j_res.reasoning[:150]}...")  # print snippet
    print(f"  Average factual correctness: {round(avg_score,2)}\n")
