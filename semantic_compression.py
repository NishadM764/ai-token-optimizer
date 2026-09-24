from openai import OpenAI


class SemanticCompressionModule:

    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    def compress(
        self,
        prompt: str,
        model: str = "openrouter/free"
    ) -> str:

        if not prompt.strip():
            return ""

        system_message = (
            "Compress the user's prompt to maximize token efficiency "
            "while preserving its original meaning, constraints, "
            "requirements, and intent. "
            "Remove unnecessary words and repetition. "
            "Keep all important information. "
            "Output ONLY the compressed prompt."
        )

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

            if response.choices:
                result = response.choices[0].message.content

                if result:
                    return result.strip()

            return "Error: Empty response from OpenRouter."

        except Exception as e:
            return f"Error: {str(e)}"