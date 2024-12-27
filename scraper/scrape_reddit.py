import praw
import config

#configure praw
reddit = praw.Reddit(
    client_id = config.client_id,
    client_secret = config.client_secret,
    password = config.password,
    username = config.username,
    user_agent = config.user_agent,
)


#helper that returns title, user, and body in dict
def get_title_user_and_body(submission: praw.models.Submission) -> dict:
    return {
        "title" : submission.title,
        "user" : submission.author,
        "body" : submission.selftext
    }


#get url from user, set as submission
url: str = input()

submission: praw.models.Submission = reddit.submission(url=url)

post = get_title_user_and_body(submission)

print(post)