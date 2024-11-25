from app.database.databaser import db
from app.eyes.blip_see import blip_see
import app.openai_client as openai_client


async def caption_images(username: str) -> dict:
    captions = {}
    try:
        # Search the db for the username
        user_data = await db.get_profile_by_username(username)  # Assuming this is an async function
        
        # Check if avatar_caption is empty and caption it if necessary
        if not user_data["profile"].get("avatarCaption"):
            avatar_url = user_data["profile"].get("avatar", "")
            if avatar_url:
                # avatar_caption = blip_see(avatar_url)  # Assuming blip_see is or will be async
                avatar_caption = await openai_client.gpt4o_image_url_to_text(avatar_url, "Describe this image. It's a profile pic of a TikTok user.")
                captions["avatarCaption"] = avatar_caption
                await db.update_user_avatar_caption(username, avatar_caption)  # Assuming this is an async function
        
        updated_posts = []
        for post in user_data.get("posts", []):
            post_id = post.get("id", "")
            if not post.get("videoMeta", {}).get("coverCaption"):
                cover_url = post.get("videoMeta", {}).get("coverUrl", "")
                if cover_url:
                    print(f"Processing cover URL for post {post_id}: {cover_url}")  # Debugging line
                    cover_caption = blip_see(cover_url)  # Assuming blip_see is or will be async
                    cover_caption = await openai_client.gpt4o_image_url_to_text(cover_url, "Describe this image. It's the cover image of a TikTok post.")

                    print(f"Generated caption for post {post_id}: {cover_caption}")  # Debugging line
                    post["videoMeta"]["coverCaption"] = cover_caption
                    captions[post_id] = cover_caption
            updated_posts.append(post)
            
        # Update the user's posts with the new captions
        await db.update_user_info(username, {"posts": updated_posts})  # Assuming this is an async function
    except Exception as e:
        print(f"Error captioning images: {e}")

    return captions

