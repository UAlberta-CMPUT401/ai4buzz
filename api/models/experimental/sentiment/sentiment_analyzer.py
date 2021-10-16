from api.models.feature_analyzer import FeatureAnalyzer

class SentimentAnalyzer(FeatureAnalyzer):
    def get_descriptions(self, image):
        return super().get_descriptions(image)

    def _format_description(self, description):
        return super()._format_description(description)
