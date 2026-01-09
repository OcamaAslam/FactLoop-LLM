import re
from llm_utils import get_llm_response

def parse_score(response):
    """Extracts a float score (0.0-1.0) from the LLM response using regex."""
    try:
        match = re.search(r"0\.\d+|1\.0|0|1", response)
        if match:
            return float(match.group())
        return 0.5
    except Exception:
        return 0.5

def llm_judge_score(prompt):
    """Generates a score using a low-temperature LLM call."""
    scoring_messages = [{"role": "user", "content": prompt}]
    response = get_llm_response(scoring_messages, temp=0.1)
    return parse_score(response)

def evaluate_factuality(question, knowledge):
    """Rates the factuality of the knowledge relative to the question."""
    prompt = f"""Role: Medical Fact Checker.
    Task: Rate the factuality of the Knowledge relative to the Question.
    Score range: 0.0 (Irrelevant) to 1.0 (Highly Factual).
    Question: {question}
    Knowledge: {knowledge}
    Output ONLY the numeric score."""
    return llm_judge_score(prompt)

def evaluate_consistency(question, response, knowledge):
    """Rates consistency and entailment of the response."""
    cons_prompt = f"""Role: Consistency Checker.
    Task: Check if the Response is supported by the Knowledge.
    Score range: 0.0 (Contradicts) to 1.0 (Fully supported).
    Knowledge: {knowledge}
    Response: {response}
    Output ONLY the numeric score."""
    
    entail_prompt = f"""Task: Rate how well the Response directly answers the Question.
    Score: 0.0 to 1.0.
    Question: {question}
    Response: {response}
    Output ONLY the numeric score."""
    
    consistency_score = llm_judge_score(cons_prompt)
    entailment_score = llm_judge_score(entail_prompt)
    
    return entailment_score, consistency_score