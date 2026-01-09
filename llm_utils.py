import time
from config import client, MODEL_NAME

def get_llm_response(messages, temp=0.7):
    
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=4096,
                temperature=temp,
                stream=False
            )

            message = completion.choices[0].message
            content = message.content

            # Log reasoning if present (common in some reasoning models)
            if hasattr(message, 'reasoning_content') and message.reasoning_content:
                print(f"[Model Reasoning]: {message.reasoning_content}...")

            if not content or not content.strip():
                print(f"[Attempt {attempt+1}] Model returned empty text. Retrying...")
                time.sleep(1)
                continue

            return content

        except Exception as e:
            print(f"[Attempt {attempt+1} Error]: {e}")
            time.sleep(1)

    return "[ERROR: Model failed to generate text after 3 attempts]"