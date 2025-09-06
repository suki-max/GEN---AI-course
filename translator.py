from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

class Translator:
    def __init__(self):
        model_name = 'facebook/mbart-large-50-many-to-many-mmt'
        self.tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
        self.model = MBartForConditionalGeneration.from_pretrained(model_name)

    def translate(self, text, src_lang: str, tgt_lang: str):
        self.tokenizer.src_lang = src_lang
        encoded = self.tokenizer(text, return_tensors='pt')
        generated = self.model.generate(**encoded, forced_bos_token_id=self.tokenizer.lang_code_to_id[tgt_lang])
        return self.tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
