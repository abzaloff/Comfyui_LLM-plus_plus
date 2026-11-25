class LLMPlusUserPrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "positive": (
                    "STRING",
                    {"default": "", "multiline": True, "dynamicPrompts": False},
                ),
                "enable_translate": ("BOOLEAN", {"default": True}),
                "from_translate": (["auto", "ru", "en"], {"default": "ru"}),
                "to_translate": (["en", "ru"], {"default": "en"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("positive",)
    FUNCTION = "process"
    CATEGORY = "LLM++"
    DESCRIPTION = "Pass a user prompt through or translate it into English or Russian."

    def process(self, positive, enable_translate, from_translate, to_translate):
        text = str(positive or "")
        if not enable_translate or not text.strip() or from_translate == to_translate:
            return (text,)

        if from_translate not in ("auto", "ru", "en"):
            raise ValueError(f"Unsupported source language: {from_translate}")
        if to_translate not in ("ru", "en"):
            raise ValueError(f"Unsupported target language: {to_translate}")

        try:
            from googletrans import Translator
        except ImportError as error:
            raise RuntimeError(
                "User_Prompt translation requires googletrans-py==4.0.0. "
                "Install the custom node's requirements.txt and restart ComfyUI."
            ) from error

        translator = Translator(raise_exception=True, timeout=20.0)
        try:
            result = translator.translate(text, src=from_translate, dest=to_translate)
            translated = str(result.text or "")
            if not translated.strip():
                raise ValueError("Translation returned empty text.")
            return (translated,)
        finally:
            translator.client.close()
