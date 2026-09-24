import json
from openai import OpenAI


class PromptQualityAnalysisModule:

    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    def analyze_quality(
        self,
        prompt: str,
        model: str = "openrouter/free"
    ) -> dict:

        if not prompt.strip():
            return {"error": "Prompt is empty"}

        system_message = """
Evaluate the user's prompt on:

1. Clarity
2. Relevance
3. Specificity
4. Structure
5. Redundancy

Give each dimension a score from 1 to 5.

Also provide:
- Overall feedback
- Suggested fix

Return ONLY a valid JSON object using exactly this structure:

{
    "clarity": {
        "score": 1,
        "justification": ""
    },
    "relevance": {
        "score": 1,
        "justification": ""
    },
    "specificity": {
        "score": 1,
        "justification": ""
    },
    "structure": {
        "score": 1,
        "justification": ""
    },
    "redundancy": {
        "score": 1,
        "justification": ""
    },
    "overall_feedback": "",
    "suggested_fix": ""
}

The score must be an integer from 1 to 5.
Do not use Markdown.
Do not wrap the JSON in code fences.
"""

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.0
            )

            if not response.choices:
                return {
                    "error": "No response received from OpenRouter."
                }

            raw_text = response.choices[0].message.content.strip()

            if "```json" in raw_text:
                raw_text = (
                    raw_text
                    .split("```json", 1)[1]
                    .split("```", 1)[0]
                    .strip()
                )

            elif "```" in raw_text:
                raw_text = (
                    raw_text
                    .split("```", 1)[1]
                    .split("```", 1)[0]
                    .strip()
                )

            return json.loads(raw_text)

        except json.JSONDecodeError as e:
            return {
                "error": f"Invalid JSON returned by AI: {str(e)}"
            }

        except Exception as e:
            return {
                "error": f"Error parsing or calling API: {str(e)}"
            }