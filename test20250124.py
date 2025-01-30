import string
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import os
import emoji

# import matplotlib.pyplot as plt
import csv
import re

_RE_COMBINE_WHITESPACE = re.compile(r"\s+")

from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

nltk.download("stopwords")
nltk.download("punkt_tab")
stop_words = set(stopwords.words("english"))


comments = pd.read_csv(
    os.path.join("polished_data", "comments_from_videos.csv"),
    dtype={
        "id": "Int64",
        "video_id": "Int64",
        "author": object,
        "date": "Int64",
        "likes": "Int64",
        "replies": "Int64",
        "reply_of": "Int64",
        "text": object,
    },
)

# print(comments.shape[0])

actual_comments = comments.loc[~comments.text.isna()]

emoji_counts = pd.DataFrame(
    {
        "emojis": actual_comments.text.apply(lambda s: emoji.emoji_count(s)),
        "Length": actual_comments.text.apply(len),
    }
)

# x = emoji_counts.emojis / emoji_counts.Length

# print(np.quantile(x, [.9,.91,.92,.93,.94]))
# print(np.mean(x))

# plt.hist(x, cumulative=True)
# plt.show()

# print(np.quantile(emoji_counts.Length, [0,.25,.5,.75,1]))
# print(np.quantile(emoji_counts.emojis, [0,.25,.5,.75,1]))

# Soglia cambiabile
actual_comments_2 = actual_comments.loc[emoji_counts.emojis / emoji_counts.Length < 0.2]
actual_comments_2.text = actual_comments_2.text.apply(lambda s: s.lower())
actual_comments_2["text_no_stopwords"] = actual_comments_2.text.apply(
    lambda s: _RE_COMBINE_WHITESPACE.sub(
        " ",
        emoji.replace_emoji(
            " ".join([w for w in word_tokenize(s) if w not in stop_words]), replace=""
        ).translate(str.maketrans("", "", string.punctuation + "‘’“”«»–—")),
    ).strip()
)

actual_comments_2.to_csv(
    os.path.join("polished_data", "clean_comments.csv"),
    index=False,
    quoting=csv.QUOTE_NONNUMERIC,
)
