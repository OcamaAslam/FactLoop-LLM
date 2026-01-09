from loops import knowledge_loop, response_loop

def run_test():
    print("System Ready. Full debug mode enabled.")
    
    while True:
        try:
            q = input("\nEnter Question (or 'q' to exit): ")
            if q.lower() in ['q', 'exit']:
                break
            
            print(f"\n{'#'*60}\nQUESTION: {q}\n{'#'*60}")
            
            final_knowledge = knowledge_loop(q)
            final_answer = response_loop(q, final_knowledge)
            
            print(f"\nFINAL APPROVED ANSWER:\n{final_answer}\n")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_test()