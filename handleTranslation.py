from googletrans import Translator


class HandleTranslation:

    def __init__(self, translationLanguage):
        self.translator = Translator()
        self.translationLanguage = translationLanguage
    def translate(self, message):
        try:
            translatedMessage = self.translator.translate(message, dest=self.translationLanguage).text
        except Exception as e:
            translatedMessage = message
        return translatedMessage

