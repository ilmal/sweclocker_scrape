import pandas as pd
import os

dirname = os.path.dirname(__file__)
db_path = os.path.join(dirname, "../../posts.csv")

def check_db(post_urls):

    # read dataframe
    df = pd.read_csv(db_path, index_col=0)
    
    new_indexes = []
    for i, post in enumerate(post_urls):
        if post in df["post_url"].values.tolist():
            continue
        new_indexes.append(i)
    return new_indexes