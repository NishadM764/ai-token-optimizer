import re


class PromptCompressionModule:

    def compress(self, prompt: str) -> str:
        if not prompt.strip():
            return ""

        # Remove unnecessary whitespace
        compressed = re.sub(r"\s+", " ", prompt).strip()

        # Remove common filler phrases
        filler_phrases = [
            r"\bplease\b",
            r"\bkindly\b",
            r"\bi would like you to\b",
            r"\bi want you to\b",
            r"\bcan you please\b",
            r"\bcould you please\b",
            r"\bif possible\b",
        ]

        for phrase in filler_phrases:
            compressed = re.sub(
                phrase,
                "",
                compressed,
                flags=re.IGNORECASE
            )

        # Remove repeated spaces after deletion
        compressed = re.sub(r"\s+", " ", compressed).strip()

        return compressed