from groq import Groq
from src.config import Config
from src.hindsight_client import HindsightMemoryClient

class SerenovaEAPAgent:
    def __init__(self):
        Config.validate()
        self.llm_client = Groq(api_key=Config.GROQ_API_KEY)
        self.memory_layer = HindsightMemoryClient()

    def _get_system_prompt(self, historical_context: str) -> str:
        base_prompt = (
            "You are Serenova, an elite corporate EAP (Employee Assistance Program) AI companion.\n"
            "Your objective is to mitigate workplace burnout, anxiety, and operational stress.\n"
            "Tone guidelines: Empathetic, calm, non-judgmental, psychologically grounding, and highly professional.\n"
            "CRITICAL: Avoid generic clinical platitudes. Ground your advice in the user's historic timeline.\n"
        )
        
        if historical_context:
            base_prompt += (
                f"\n[CRITICAL HINDSIGHT MEMORY CONTEXT FOUND]\n"
                f"The following historical context has been securely retrieved via Hindsight from previous sessions "
                f"with this specific worker token. Use these facts to notice long-term structural patterns, "
                f"follow up on past milestones, or re-apply past coping mechanisms that previously worked:\n"
                f"{historical_context}\n"
                f"Do not explicitly tell the user 'According to your historical database logs', weave this memory "
                f"naturally into your dialogue like an attentive coach who remembers past interactions."
            )
        else:
            base_prompt += "\nNo prior history exists for this worker token. Establish a welcoming foundational baseline."
            
        return base_prompt

    def interact(self, user_token: str, user_message: str) -> str:
        # Step 1: Query Hindsight to bring past sessions into context
        historical_context = self.memory_layer.recall_historical_context(user_token, user_message)
        
        # Step 2: Formulate dynamic prompt payload for LLM execution
        system_instructions = self._get_system_prompt(historical_context)
        
        messages = [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_message}
        ]
        
        # Step 3: Run Inference through Groq
        chat_completion = self.llm_client.chat.completions.create(
            messages=messages,
            model=Config.LLM_MODEL,
            temperature=0.7,
            max_tokens=512
        )
        
        agent_response = chat_completion.choices[0].message.content
        
        # Step 4: Background Thread/Asynchronous Summary extraction to update Hindsight memory
        self._update_hindsight_pipeline(user_token, user_message, agent_response)
        
        return agent_response

    def _update_hindsight_pipeline(self, user_token: str, user_message: str, agent_response: str):
        """
        Distills current interactions into actionable, structured long-term memory points
        to push upstream into Hindsight.
        """
        summary_prompt = (
            f"Analyze the following conversation block and isolate core tracking metrics:\n"
            f"User input: {user_message}\n"
            f"Agent response: {agent_response}\n\n"
            f"Extract updates on: Workplace stressors, scheduling triggers, biological symptoms (e.g., sleep loss), "
            f"and strategies accepted/rejected. Write a short, highly condensed 2-sentence structural progress insight."
        )
        
        completion = self.llm_client.chat.completions.create(
            messages=[{"role": "user", "content": summary_prompt}],
            model=Config.LLM_MODEL,
            temperature=0.3,
            max_tokens=150
        )
        
        distilled_memory = completion.choices[0].message.content
        # Save into Hindsight persistence instance
        self.memory_layer.store_interaction_memory(user_token, distilled_memory)