class PromptBuilder:
    def build(self, context: dict) -> str:
        input_text = context.get("input", "")
        knowledge = context.get("knowledge", {})

        documents = knowledge.get("documents", [])

        knowledge_text = self._build_knowledge_block(documents)

        # 🔥 КЛЮЧЕВОЙ МОМЕНТ
        if knowledge_text:
            return f"""
You are an AI assistant.

STRICT RULE:
You MUST answer ONLY using the provided context.

If the answer is NOT in the context → respond EXACTLY:
"I don't know based on the provided context."

Context:
{knowledge_text}

Question:
{input_text}

Answer:
""".strip()

        # fallback
        return f"""
You are an AI assistant.

No external knowledge is available.

Answer briefly:

Question:
{input_text}

Answer:
""".strip()

    def _build_knowledge_block(self, documents: list) -> str:
        if not documents:
            return ""

        texts = []

        for doc in documents:
            text = doc.get("text", "")
            if text:
                texts.append(text.strip())

        # ограничение
        texts = texts[:3]

        return "\n\n---\n\n".join(texts)