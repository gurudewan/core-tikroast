import json
from pprint import pprint

from app.database.databaser import db

from datetime import datetime

def map_profile(username, raw_profile_scrape):
    if not raw_profile_scrape or not isinstance(raw_profile_scrape, list) or not raw_profile_scrape[0]:
        raise ValueError("Invalid raw_profile_scrape data")
    try:

        profile_info = raw_profile_scrape[0].get('authorMeta', {})

        posts = extract_posts(raw_profile_scrape)

        user_data = {
            "username": username,
            "analysis": {
            },
            "profile": {
                "id": profile_info.get("id", ""),
                "name": profile_info.get("name", ""),
                "nickName": profile_info.get("nickName", ""),
                "verified": profile_info.get("verified", False),
                "signature": profile_info.get("signature", ""),
                "bioLink": profile_info.get("bioLink", ""),
                "avatar": profile_info.get("avatar", ""),
                "avatarCaption": None,
                "privateAccount": profile_info.get("privateAccount", False),
                "region": profile_info.get("region", ""),
                "following": profile_info.get("following", 0),
                "friends": profile_info.get("friends", 0),
                "fans": profile_info.get("fans", 0),
                "heart": profile_info.get("heart", 0),
            },
            "posts": posts,
            "scraped_info": {
                "raw_profile": raw_profile_scrape,
                "raw_comments": None
            },
            "scrape_meta_info": {
                "scrape_timestamp": datetime.now()
            }
        }

        db.create_new_user(user_data)
    except Exception as e:
        print(f"Error mapping profile: {e}")


def extract_posts(raw_profile):
    posts = []
    for post in raw_profile:
        try:
            post_data = {
                "id": post.get("id", ""),
                "text": post.get("text", ""),
                "createTimeISO": post.get("createTimeISO", ""),
                "musicMeta": post.get("musicMeta", {}),
                "webVideoUrl": post.get("webVideoUrl", ""),
                "videoMeta": {
                    "duration": post.get("videoMeta", {}).get("duration", 0),
                    "coverUrl": post.get("videoMeta", {}).get("coverUrl", ""),
                    "coverCaption": None
                },                
                "diggCount": post.get("diggCount", 0),
                "shareCount": post.get("shareCount", 0),
                "playCount": post.get("playCount", 0),
                "collectCount": post.get("collectCount", 0),
                "commentCount": post.get("commentCount", 0),
                "mentions": post.get("mentions", []),
                "hashtags": post.get("hashtags", []),
                "effectStickers": post.get("effectStickers", []),
                "isSlideshow": post.get("isSlideshow", False),
                "isPinned": post.get("isPinned", False),
            }
            posts.append(post_data)
        except Exception as e:
            print(f"Error processing post: {e}")
            pass
    return posts