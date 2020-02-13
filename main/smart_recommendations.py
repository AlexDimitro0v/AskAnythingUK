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

    return most_common


def get_recommended_feedbackers(words1,frequencies1):
    recommended_users = []
    for user in User.objects.all():
        words2 = user.userprofile.most_common_words
        frequencies2 = user.userprofile.most_common_words_numbers
        if not words2: continue
        if len(frequencies2) < len(words2): continue
        total = 0
        w1_square = 0
        w2_square = 0
        for i in range(0,len(words1)):
            for j in range(0,len(words2)):
                if words1[i][0] == words2[j][0]:
                    total += frequencies1[1]*frequencies2[1]
            w1_square += frequencies1[i]**(2)
            w2_square += frequencies2[i]**(2)
        total = total/(w1_square**(1/2) * w2_square**(1/2))
        if total > 0.3:
            print(user)
            recommended_users.append(user)
    return recommended_users
