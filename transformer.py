from transformers import pipeline
import json
import youtube_parser as ytp

# ytp.get_all_yt_video_comments(ytp.get_all_video_ids())
# y_part = ytp.get_comments_as_list()

y_part = []

classifier = pipeline("sentiment-analysis")

good_counter = 0
bad_counter = 0
def classify_comments(comments: list):
    global good_counter, bad_counter
    for i in comments:
        result = classifier(i)
        if result[0]['label'] == 'POSITIVE':
            good_counter += 1
        else:
            bad_counter += 1
    return good_counter, bad_counter

print(classify_comments(y_part))