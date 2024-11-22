import logging
from app.fastAPI_config import app # the fastAPI app

import app.analyser as analyser
#import app.scrapers.apify_scraper as scraper

import app.scraping.apify.tiktok as tiktok_scraper

import app.eyes.blip_see as see
import time
from pprint import pprint

import app.scraping.schema_mapper as schema_mapper

import app.eyes.processor as processor

from app.database.databaser import db

from typing import List
from fastapi import Query
from fastapi import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.get("/analyse-me")
async def analyse_me(username: str):
    try:
        logger.info(f"Starting analysis for username: {username}")
        # check if analysis already exists
        if not db.analysis_exists(username):
            logger.info(f"No existing analysis found for username: {username}")
            # ===== begin new analysis of profile ====
            if not db.scraping_exists(username):
                logger.info(f"No scraping data found for username: {username}")
                start_time = time.time()
                # scrape the profile on tik tok
                scraped_info = tiktok_scraper.do_scrape(username)
                logger.info(f"Scraping completed for username: {username}")
                # convert the profile to our schema, and store in db
                schema_mapper.map_profile(username, scraped_info['profile_scrape'])
                end_time = time.time()
                duration = end_time - start_time
                logger.info(f"Scraping duration for username '{username}': {duration:.2f} seconds")

             # generate the analysis of the profile
            start_time_analysis = time.time()
            analysis_result = await analyser.analyse(username)
            end_time_analysis = time.time()
            duration_analysis = end_time_analysis - start_time_analysis
            logger.info(f"Profile analysis duration for username {username}: {duration_analysis:.2f} seconds")
            # place the analysis result into db
            db.store_analysis(username, analysis_result)
            logger.info(f"Analysis stored in DB for username: {username}")
        
        profile = db.get_profile_by_username(username)
        return profile

    except Exception as e:
        logging.error(f"Error during analysis: {e}")
        return {"error": "An error occurred during analysis. Please try again later."}


@app.get("/get-profiles")
async def get_profiles(usernames: str = Query(...)):

    try:
        usernames_list = usernames.split(',')
        logger.info(f"Fetching profiles for usernames: {usernames_list}")

        profiles = db.get_profiles_by_usernames(usernames_list)
        logger.info(f"Retrieved profiles for usernames: {usernames_list}")

        return profiles

    except Exception as e:
        logger.error(f"Error fetching profiles for usernames {usernames_list}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching profiles. Please try again later.")