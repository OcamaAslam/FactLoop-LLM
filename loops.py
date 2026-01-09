from config import args
from llm_utils import get_llm_response
from evaluation import evaluate_factuality, evaluate_consistency

def knowledge_loop(question):
    
    print("\n--- Step 1: Knowledge Generation ---")

    # 1 Draft
    prompt = f"Provide medical background knowledge to answer: {question}"
    knowledge = get_llm_response([{"role": "user", "content": prompt}], temp=args.temperature)

    print(f"\n[Draft Knowledge]:\n{knowledge}\n")

    score = evaluate_factuality(question, knowledge)
    print(f"Factuality Score: {score}")

    # 2 Refine
    loop_i = 0
    while loop_i < args.max_knowledge_loop and score < args.threshold_fact:
        print(f"\nScore {score} is below threshold. Refining knowledge...")

        feedback = f"The previous knowledge was rated {score}/1.0. Refine it to be strictly factual."
        knowledge = get_llm_response([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": knowledge},
            {"role": "user", "content": feedback}
        ], temp=args.temperature)

        print(f"\n[Refined Knowledge {loop_i+1}]:\n{knowledge}\n")

        score = evaluate_factuality(question, knowledge)
        print(f"New Factuality Score: {score}")
        loop_i += 1

    return knowledge

def response_loop(question, knowledge):
    """
    Generates and refines the final answer until it meets the consistency threshold.
    """
    print("\n--- Step 2: Answer Generation ---")

    # 1 Draft
    prompt = f'''Using this knowledge: "{knowledge}", answer the question: "{question}"'''
    response = get_llm_response([{"role": "user", "content": prompt}], temp=args.temperature)

    print(f"\n[Draft Answer]:\n{response}\n")

    entailment, consistency = evaluate_consistency(question, response, knowledge)
    print(f"Consistency: {consistency} | Relevance: {entailment}")

    # 2 Refine
    loop_i = 0
    while loop_i < args.max_response_loop and consistency < args.threshold_cons:
        print(f"\nConsistency {consistency} is below threshold. Refining answer...")

        feedback = "The answer is not fully supported by the provided knowledge. Fix it."
        response = get_llm_response([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response},
            {"role": "user", "content": feedback}
        ], temp=args.temperature)

        print(f"\n[Refined Answer {loop_i+1}]:\n{response}\n")

        entailment, consistency = evaluate_consistency(question, response, knowledge)
        print(f"New Consistency: {consistency} | Relevance: {entailment}")
        loop_i += 1

    return response