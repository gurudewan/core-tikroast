
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


@app.get("/get-profiles")
async def get_profiles(usernames: str = Query(...)):

    usernames_list = usernames.split(',')
    profiles = db.get_profiles_by_usernames(usernames_list)

    return profiles


