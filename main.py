from youtube_parser import get_all_yt_video_comments, get_all_video_ids, get_comments_as_list, post_vids
from llama import get_responce_llama, get_result_stats, generate_response
import time
import matplotlib.pyplot as plt

positive_list = ["Yes", "yes", "positive"]
negative_list = ["No", "no", "negative"]

def main():
    print("Programm started")
    post_vids("#programming", "#python")
    time.sleep(3)
    get_all_yt_video_comments(get_all_video_ids())
    time.sleep(10)
    integer_mark_list = []
    print(get_comments_as_list())
    comment_list = get_comments_as_list()
    for i in comment_list:
        llama_responce = get_responce_llama(prompt=str(i))
        llama_responce = llama_responce.split()
        for j in range(len(llama_responce)):
            if llama_responce[j] in positive_list:
                integer_mark_list.append("1")
                break
            elif llama_responce[j] in negative_list:
                integer_mark_list.append("-1")
                break
            elif llama_responce[j] == llama_responce[-2]:
                integer_mark_list.append("0")
    
    print(integer_mark_list)
    variants_list = ["1", "-1", "0"]
    percent_list = get_result_stats(integer_mark_list)
    plt.pie(percent_list, labels=variants_list, autopct='%1.1f%%')
    plt.axis("equal")
    plt.show()

def main_test(prompt):
    print(generate_response(prompt))



if __name__ == '__main__':
    main_test("Type a number from 1 to 10")
