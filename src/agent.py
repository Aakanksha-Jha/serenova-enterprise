from groq import Groq
from config import Config
from hindsight_client import HindsightMemoryClient

class SerenovaEAPAgent:
    def __init__(self):
        Config.validate()
        self.llm_client = Groq(
            api_key=Config.GROQ_API_KEY,
            base_url="https://api.cerebras.ai/v1"
        )
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

    def interact(self, worker_token: str, user_message: str) -> str:
        # 1. Fetch relevant memory context using your existing hindsight client
        context = ""
        try:
            memories = self.memory_layer.query_memory(worker_token, user_message)
            if memories:
                context = "\n".join([m.get("text", "") for m in memories])
        except Exception as e:
            print(f"Memory layer retrieval skipped: {e}")

        # 2. Build the message array
        messages = [
            {"role": "system", "content": f"You are Serenova, a secure corporate EAP wellness agent. Help the user manage stress. Relevant past context:\n{context}"},
            {"role": "user", "content": user_message}
        ]

        # 3. Direct HTTP request straight to Cerebras (bypassing SDK mapping bugs)
        import streamlit as st
        import os
        import requests

        raw_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
        api_key = str(raw_key).strip()

        # Build clean OpenRouter compliant headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://streamlit.app", # Required by OpenRouter
            "X-Title": "Serenova Enterprise"
        }
        
        payload = {
            "model": "openai/gpt-oss-120b:free", # High-reasoning free tier model
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.7
        }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result_json = response.json()
            return result_json["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Inference Error: {str(e)}. Please check your Streamlit secrets setup."

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