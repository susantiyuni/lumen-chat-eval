from textwrap import dedent
from judges.base import BaseJudge, Judgment

class FactualGradeJudge(BaseJudge):
    """
    Judge an LLM response for factual correctness and assign a score from 1 to 5:
        1 - Completely wrong / hallucinated
        2 - Mostly incorrect
        3 - Partially correct
        4 - Mostly correct
        5 - Fully correct
    """
    def __init__(self, model):
        super().__init__(model=model)

    def judge(self, input: str, output: str = None, expected: str = None) -> Judgment:
        system_prompt = None
        user_prompt = dedent(
            f"""
            You are an AI judge. Evaluate the factual correctness of the response
            based on the input. Assign a **score from 1 to 5**:

                1 - Completely wrong / hallucinated
                2 - Mostly incorrect
                3 - Partially correct
                4 - Mostly correct
                5 - Fully correct

            Explain your reasoning briefly.

            Input: {input}
            Response: {output}

            Respond ONLY in JSON format:
            {{
                "reasoning": "...",
                "score": 1  # integer 1-5
            }}
            """
        )

        reasoning, score = self._judge(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
        )

        # Convert score to int if returned as string
        try:
            score = int(score)
        except:
            score = 0  # fallback if parsing failed

        return Judgment(reasoning=reasoning, score=score, score_type="numerical")
