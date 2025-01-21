INSTRUCTIONS = {
    'en':
    """Question: {question}
Please provide your best answer to this question in Hungarian and indicate your confidence in your answer using a score from 0 to 100. Please provide your response in the following JSON format:
{
    "answer": "Your answer here",
    "confidence_score": number
}
""",
    'hu':
    """Kérdés: {question}
Kérjük, magyar nyelven adja meg a legjobb választ erre a kérdésre, és 0-tól 100-ig terjedő pontszámmal jelezze, hogy bízik a válaszában. Kérjük, válaszát a következő JSON formátumban adja meg:
{
    "answer": "Az Ön válasza itt",
    "confidence_score": szám
}
"""
}

DATA_PATH = 'data/OpenHuEval/data/HuSimpleQA.jsonl'
