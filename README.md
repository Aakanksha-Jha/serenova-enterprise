# Serenova: AI-Powered Enterprise Employee Assistance Program (EAP) Agent

Serenova is a memory-augmented, enterprise-grade mental wellness and burnout prevention agent designed for corporate environments. Built for the Vectorize Memory Hackathon, it solves the core flaw of traditional Employee Assistance Programs: static, forgetful, and disconnected interactions.

Using **Hindsight**, Serenova securely retains contextual awareness of an employee's ongoing workplace stressors, triggers, and historically effective coping mechanisms over months without compromising individual privacy.

## Features
- **Hindsight-Powered Persistent Memory:** Tracks user stressors across multi-week intervals to surface burnout patterns.
- **Privacy-Preserving Design:** Uses de-identified cryptographic tokens instead of corporate PII.
- **Dynamic Context Injection:** Automatically balances current user state with historically effective remedies.

## Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and populate your API credentials.
4. Run the simulation pipeline: `python src/main.py`