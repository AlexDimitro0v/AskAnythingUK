import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from users.models import UserProfile
from django.contrib.auth.models import User


def get_most_common(text):
    # First conert everything to lowercase
    text = text.lower()
    # Extract individual words from text
    tokens = word_tokenize(text)

    # Remove stopwords and punctuation from text
    stop_words = stopwords.words('english')
    clean_tokens = []
    for token in tokens:
        if token not in stop_words and token not in list(".,():[]{}!%&?") and token[0] != "'":
            clean_tokens.append(token)

    # Lemmatize all remaining words as nouns
    lemmatizer = WordNetLemmatizer()
    for i in range(len(clean_tokens)):
        if clean_tokens[i] != "us":
            clean_tokens[i] = lemmatizer.lemmatize(clean_tokens[i], pos="n")

    # Get the frequency distribution of words and take the 30 most common words
    freq = nltk.FreqDist(clean_tokens)
    most_common = freq.most_common(30)
    most_common_list = []
    for w in most_common:
        most_common_list.append(w[0])

    return most_common_list


def get_recommended_feedbackers(words1):
    recommended_users = []
    for user in User.objects.all():
        matches = 0
        for w in user.userprofile.most_common_words:
            if w in words1:
                matches += 1
        if matches >= 5:
            recommended_users.append(user)
    return recommended_users
