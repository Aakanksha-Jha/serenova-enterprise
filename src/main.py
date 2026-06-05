import time
from agent import SerenovaEAPAgent

def run_hackathon_demo_simulation():
    print("=========================================================================")
    print(" SERENOVA ENTERPRISE: MULTI-SESSION HINDSIGHT DEMO SIMULATION ")
    print("=========================================================================\n")

    # Initialize Agent
    agent = SerenovaEAPAgent()
    
    # Secure token tracking a single worker's lifetime over weeks
    worker_token = "token_hash_usr_9a87f1c4e2b0"

    # --- SESSION 1: The Initial Crisis ---
    print("--- [TIMELINE: WEEK 1] Interaction 1: Software Launch Stress ---")
    user_input_1 = "I am completely overwhelmed. This new production deployment cycle is keeping me up until 3 AM, and my engineering lead keeps adding scopes to our current sprint. I'm exhausted."
    print(f"Employee: {user_input_1}\n")
    
    # Simulate historical trace mock fallback injection for standalone showcase runs
    agent.memory_layer.store_interaction_memory(
        worker_token, 
        "Worker experiencing severe sleep deprivation (sleeping at 3 AM) driven by a software production launch timeline and scope creep from team lead."
    )
    
    response_1 = agent.interact(worker_token, user_input_1)
    print(f"Serenova AI:\n{response_1}\n")
    print("-" * 80)
    
    # Wait a simulated interval to differentiate blocks
    time.sleep(1)

    # --- SESSION 2: Checking Back In After Weeks ---
    print("\n--- [TIMELINE: WEEK 3] Interaction 5: Following Up On Milestones ---")
    user_input_2 = "Hey, I'm logging in again. I feel anxious today, my chest feels a bit tight."
    print(f"Employee: {user_input_2}\n")
    
    # Reinforce the memory bank with context about past sprints
    agent.memory_layer.store_interaction_memory(
        worker_token, 
        "Worker historical stress spikes align with sprint review timelines occurring on the third week of the month."
    )
    
    response_2 = agent.interact(worker_token, user_input_2)
    print(f"Serenova AI:\n{response_2}\n")
    print("-" * 80)
    
    time.sleep(1)

    # --- SESSION 3: Multi-Week Structural Trend Identification ---
    print("\n--- [TIMELINE: WEEK 6] Interaction 20: Pattern Recognition ---")
    user_input_3 = "It's that time of the month again. Just feeling total dread about presentation loops tomorrow."
    print(f"Employee: {user_input_3}\n")
    
    response_3 = agent.interact(worker_token, user_input_3)
    print(f"Serenova AI:\n{response_3}\n")
    print("=========================================================================")

if __name__ == "__main__":
    # Standard entry execution route
    run_hackathon_demo_simulation()