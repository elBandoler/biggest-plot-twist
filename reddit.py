import praw
import json
import os

# הגדרות API – שים את הערכים שלך כאן
client_id = ''
client_secret = ''
user_agent = 'reddit-test-app'

# התחברות ל-Reddit
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

def fetch_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)

    def parse_comment(comment, parent_id=None):
        return {
            'id': comment.id,
            'parent_id': parent_id,
            'author': str(comment.author),
            'body': comment.body,
            'score': comment.score,
            'created_utc': comment.created_utc,
            'replies': [parse_comment(reply, comment.id) for reply in comment.replies]
        }

    all_comments = [parse_comment(top_level) for top_level in submission.comments]
    return {
        'post_id': submission.id,
        'title': submission.title,
        'url': url,
        'comments': all_comments
    }

# === השתמש בקוד הזה ===
if __name__ == "__main__":
    post_url = input("הדבק את קישור הפוסט מרדיט: ").strip()
    data = fetch_comments(post_url)

    filename = f"reddit_{data['post_id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ נשמר בהצלחה כקובץ {filename}")
