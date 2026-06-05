import requests
from src.config import Config

class HindsightMemoryClient:
    """
    Interface wrapper interacting with Vectorize's Hindsight HTTP API/SDK ecosystem
    to handle long-term agent state persistence and context discovery.
    """
    def __init__(self):
        self.base_url = Config.HINDSIGHT_URL
        self.headers = {
            "Authorization": f"Bearer {Config.HINDSIGHT_API_KEY}",
            "Content-Type": "application/json"
        }

    def store_interaction_memory(self, user_token: str, continuous_summary: str):
        """
        Commits deep synthesized insights about workplace stress, tracking indicators,
        and chronological milestones into the Hindsight memory layer.
        """
        endpoint = f"{self.base_url}/memory/store"
        payload = {
            "namespace": "serenova_enterprise_eap",
            "key": user_token,
            "memory_chunk": continuous_summary,
            "metadata": {"source": "eap_agent_session"}
        }
        try:
            response = requests.post(endpoint, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            # Fallback mock for demonstration environments if networking credentials aren't active yet
            return False

    def recall_historical_context(self, user_token: str, current_query: str) -> str:
        """
        Queries Hindsight using vector semantic search to retrieve historical insights 
        relevant to the user's current situation.
        """
        endpoint = f"{self.base_url}/memory/recall"
        payload = {
            "namespace": "serenova_enterprise_eap",
            "key": user_token,
            "query": current_query,
            "limit": 3
        }
        try:
            response = requests.post(endpoint, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            # Extract and join recalled memories
            memories = [item.get("memory_chunk", "") for item in data.get("results", [])]
            return "\n".join(memories)
        except requests.exceptions.RequestException:
            return ""