from apify_client import ApifyClient
from app.consts import APIFY_API_KEY, COMMENTS_PER_POST, POSTS_PER_PROFILE

import app.scraping.schema_mapper as schema_mapper

def do_scrape(username):

    profile_scrape = do_profile_scrape(usernames=[username])

    return {
        "profile_scrape": profile_scrape
    }

    #top_comments = do_comments_scrape(usernames=[username])

def do_profile_scrape(usernames):
    client = ApifyClient(APIFY_API_KEY)

    run_input = { "profiles": usernames, "resultsPerPage": POSTS_PER_PROFILE, "excludePinnedPosts": False, }

    run = client.actor("clockworks/tiktok-profile-scraper").call(run_input=run_input)

    print("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])
    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append(item)
    return results


def do_comments_scrape(post_urls):
    client = ApifyClient(APIFY_API_KEY)
    run_input = { "postURLs": post_urls, "commentsPerPost": COMMENTS_PER_POST }

    run = client.actor("clockworks/tiktok-comments-scraper").call(run_input=run_input)

    print("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)


if __name__=="__main__":
    do_scrape(["apifyoffice"])