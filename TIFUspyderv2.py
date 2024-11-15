#this script has a block of code missing from line 7

import praw
import os
import random

# Set up Reddit AP..ch_size=10):
    try:
        # Get a list of TIFU posts sorted by 'top' from the past week
        tifu_posts = list(reddit.subreddit("tifu").top(time_filter="week", limit=batch_size * 5))

        # Filter for posts with a body (selftext) shorter than 1000 characters
        short_posts = [p for p in tifu_posts if p.selftext and len(p.selftext) < 1500]

        # If there aren’t enough posts, notify the user
        if len(short_posts) < batch_size:
            print(f"Only {len(short_posts)} suitable posts found. Adjusting batch size.")
            batch_size = len(short_posts)

        return random.sample(short_posts, batch_size)

    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []

# Function to save each post to a text file
def save_post_to_file(post, index):
    os.makedirs("tifu_posts", exist_ok=True)
    filename = f"tifu_posts/{index}_{post.id}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Title: {post.title}\n")
        file.write(f"Upvotes: {post.score}\n")
        file.write(f"URL: {post.url}\n\n")
        file.write(f"Content:\n{post.selftext}")
    print(f"Post saved to {filename}")

# Main batch processing function
def batch_process_posts(batch_size=10):
    posts = fetch_tifu_posts(batch_size=batch_size)
    if not posts:
        print("No posts available to process.")
        return

    for index, post in enumerate(posts, start=1):
        save_post_to_file(post, index)

# Run the batch processing with the desired number of posts
batch_process_posts(batch_size=10)  # Adjust the batch size as needed
