import logging
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

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.get("/analyse-me")
async def analyse_me(username: str):
    
    # check if analysis already exists
    if not db.analysis_exists(username):
        # ===== begin new analysis of profile ====
        if not db.scraping_exists(username):
            # scrape the profile on tik tok

            logging.info("starting scrape for " + username)
            scraped_info = tiktok_scraper.do_scrape(username)
            logging.info("finished scrape for " + username)
            # convert the profile to our schema, and store in db
            schema_mapper.map_profile(username, scraped_info['profile_scrape'])
            logging.info("finished schema map for " + username)
        
        #logging.info("starting captioning")
        
        #processor.caption_images(username)
        
        #logging.info("finished captioning")

        logging.info("starting analysis")
        # generate the analysis of the profile
        analysis_result = analyser.analyse(username)
        logging.info("finished analysis for " + username)
        # place the analysis result into db
        db.store_analysis(username, analysis_result)
    
    logging.info("finished storing")
    
    profile = db.get_profile_by_username(username)
    logging.info("returning")
    logging.info(profile)

    return profile


@app.get("/get-profiles")
async def get_profiles(usernames: str = Query(...)):

    usernames_list = usernames.split(',')
    profiles = db.get_profiles_by_usernames(usernames_list)

    return profiles