import re

def get_hashtags(post):
    return re.findall(r"#(\w+)", post)
