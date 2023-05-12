import time

from modules.web_handler import web_handler
from modules.snapchat_web import send_snapchat
from modules.database.add_db import add_db
from modules.database.check_db import check_db
from modules.story_pusher import post_story

def main():

    # get all new data from web
    print("Gathering info from sweclockers...")
    titles, post_urls, descriptions = web_handler()

    #check if all posts already exist in database
    new_indexes = check_db(post_urls)

    # sort out the new data
    titles_new, post_urls_new, descriptions_new = [], [], []
    for index in new_indexes:
        titles_new.append(titles[index])
        post_urls_new.append(post_urls[index])
        descriptions_new.append(descriptions[index])

    print("New posts: ", titles_new)

    def send_message(titles_new, post_urls_new, descriptions_new):
        for i, title in enumerate(titles_new):
            border = "\n --------------------------------------------------------------------------- \n"
            send_snapchat("Me", [border, title, descriptions_new[i], post_urls_new[i], border])


    if len(titles_new) > 0:
        send_message(titles_new, post_urls_new, descriptions_new)

        # add data to database
        add_db(post_urls_new)

def init():
    post_story()
    counter = 0
    while True:
        counter += 1
        main()
        time.sleep(20)

        if counter >= 4320:
            counter = 0
            post_story()



if __name__ == "__main__":
    init()