
from app.fastAPI_config import app # the fastAPI app

import app.analyser as analyser
#import app.scrapers.apify_scraper as scraper

import app.scraping.apify.tiktok as tiktok_scraper

import app.eyes.blip_see as see

from pprint import pprint

import app.scraping.schema_mapper as schema_mapper

import app.eyes.processor as processor

from app.database.databaser import db

from typing import List
from fastapi import Query


@app.get("/analyse-me")
async def analyse_me(username: str):
    
    # check if analysis already exists
    if not db.analysis_exists(username):
        # ===== begin new analysis of profile ====
        if not db.scraping_exists(username):
            # scrape the profile on tik tok
            scraped_info = tiktok_scraper.do_scrape(username)

            # convert the profile to our schema, and store in db
            schema_mapper.map_profile(username, scraped_info['profile_scrape'])

        print("captioning")
        processor.caption_images(username)

        # generate the analysis of the profile
        analysis_result = analyser.analyse(username)

        # place the analysis result into db
        db.store_analysis(username, analysis_result)
    
    profile = db.get_profile_by_username(username)

    print(profile)

    return profile

import os
import requests


@app.get("/get-profiles")
async def get_profiles(usernames: str = Query(...)):
    pprint(usernames)
    usernames_list = usernames.split(',')
    profiles = db.get_profiles_by_usernames(usernames_list)
    pprint(profiles)
    
    os.makedirs('demo-profiles', exist_ok=True)
    
    for profile in profiles:
        avatar_url = profile['profile']['avatar']
        response = requests.get(avatar_url)
        print(f"Downloading {avatar_url} - Status Code: {response.status_code}")  # Debug print
        if response.status_code == 200:
            file_path = f"demo-profiles/{profile['username']}.jpg"
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Saved {file_path}")  # Debug print
        else:
            print(f"Failed to download {avatar_url}")  # Debug print
    
    return profiles


