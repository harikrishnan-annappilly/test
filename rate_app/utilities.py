from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def get_star_rating(text):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    raw_rating = ((compound + 1) / 2) * 4 + 1

    final_rating = round(raw_rating)

    return max(1, min(5, final_rating))
