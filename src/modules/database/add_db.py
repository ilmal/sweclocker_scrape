import pandas as pd
import os

dirname = os.path.dirname(__file__)
db_path = os.path.join(dirname, "../../posts.csv")

def add_db(post_urls):

    print("Adding posts to database")

    # load dataframe
    df = pd.read_csv(db_path, index_col=0)

    # add posts to dataframe
    for post in post_urls:
        df = pd.concat([df, pd.DataFrame({"post_url":[str(post)]})])

    df = df.reset_index(drop=True)

    df.to_csv(db_path)
