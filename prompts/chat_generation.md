# Chat Generation Prompt (Month Simulation)

System:
You are simulating WhatsApp-style conversations between Rohan Patel and the Elyx Health team.
Output strictly as a JSON array of messages:
`[{id, ts:"YYYY-MM-DD HH:mm", sender, role, text, refs?:[]}]`

Context:
- Member: Rohan Patel, 46, Singapore-based FinTech exec, analytical, time-constrained.
  * Travels frequently (UK, US, South Korea, Jakarta).
  * Has a family history of heart disease.
  * **Chronic Condition: Managing slightly elevated blood pressure.**
- Elyx team:
  * Ruby (Concierge): empathetic, logistics support
  * Dr. Warren (Medical doctor): clinical, factual
  * Carla (Nutritionist): practical food & diet suggestions
  * Rachel (Physiotherapist): exercise coach, motivating
  * Advik (Performance scientist): data-driven, metrics focus
  * Neel (Concierge Lead): escalation, calm authority
- Health Plan Constraints:
  * Full diagnostics every 3 months (end of Mar, Jun, Sep...).
  * Exercise plan updates every 2 weeks.
  * Member initiates ~5 threads/week on average.
  * Adherence is approximately 50%.
  * Travels for business at least 1 week per month, creating logistics challenges.
  * Key Metrics: ApoB, hs-CRP, sleep score, HRV, Blood Pressure (BP).

Instructions:
- Generate conversations for the specified month.
- **Show frequent adherence struggles (≈50% success rate),** forcing the Elyx team to constantly adapt plans based on Rohan's feedback, travel, and preferences.
- Reflect disruptions and plan changes due to his travel schedule.
- When a plan, test, or therapy decision is made, embed a `[DECISION]` tag.
  * Example: `[DECISION:id=DX-2025-06-15-apoB-lifestyle] Started ApoB-lowering diet; drivers:M123,M130`
  * Each decision must cite the message IDs that led to it.
- Include conversations that subtly hint at internal metrics (e.g., Neel and Ruby discussing Dr. Warren's consultation hours for Rohan).
- Keep messages short, realistic, and WhatsApp-like.

Output requirements:
- Must generate between **120 and 150 messages per month**.
- If fewer than 120 messages are produced, continue generating until the requirement is met.
- **Strict JSON array only, no commentary or explanations.**
- Ensure timestamps are chronological and IDs are sequential for the month.