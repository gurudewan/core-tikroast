from pymongo import MongoClient
from app import consts

class Database:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_profile_by_username(self, username):
        users_collection = self.db['users']
        user_data = users_collection.find_one({'username': username})
        user_data = self.remove_objectid(user_data)
        if user_data:
            user_data.pop('scrape_meta_info', None)
            user_data.pop('scraped_info', None)
        return user_data
    
    def get_profiles_by_usernames(self, usernames):
        if not isinstance(usernames, list):
            usernames = [usernames]  # Ensure usernames is a list
        print(f"Usernames: {usernames}")
        users_collection = self.db['users']
        query = {'username': {'$in': usernames}}
        print(f"Query: {query}")
        users_data = list(users_collection.find(query))  # Convert cursor to list
        print(f"Users Data: {users_data}")
        profiles = []
        for user_data in users_data:
            user_data = self.remove_objectid(user_data)
            user_data.pop('scrape_meta_info', None)
            user_data.pop('scraped_info', None)
            profiles.append(user_data)
        return profiles
    ...

    def create_new_user(self, user_data):
        users_collection = self.db['users']
        result = users_collection.update_one(
            {'username': user_data['username']},
            {'$setOnInsert': user_data},
            upsert=True
        )
        return result.upserted_id

    def update_user_info(self, username, update_data):
        users_collection = self.db['users']
        result = users_collection.update_one(
            {'username': username},
            {'$set': update_data}
        )
        return result.modified_count
    
    def update_user_avatar_caption(self, username, avatar_caption):
        users_collection = self.db['users']
        result = users_collection.update_one(
            {'username': username},
            {'$set': {'profile.avatarCaption': avatar_caption}}
        )
        return result.modified_count
    
    def store_analysis(self, username, analysis_data):
        users_collection = self.db['users']
        result = users_collection.update_one(
            {'username': username},
            {'$set': {'analysis': analysis_data}}
        )
        return result.modified_count

    def analysis_exists(self, username):
        users_collection = self.db['users']
        analysis = users_collection.find_one({'username': username, 'analysis': {'$exists': True}})
        return analysis is not None and 'name' in analysis['analysis']
    
    def scraping_exists(self, username):
        users_collection = self.db['users']
        user_data = users_collection.find_one({'username': username})
        if user_data and 'scraped_info' in user_data and user_data['scraped_info'].get('raw_profile'):
            return bool(user_data['scraped_info']['raw_profile'])
        return False
    
    def remove_objectid(self, data):
        if isinstance(data, list):
            return [self.remove_objectid(item) for item in data]
        elif isinstance(data, dict):
            return {key: value for key, value in data.items() if key != '_id'}
        else:
            return data

db = Database(consts.MONGO_DB_STRING, 'raw-selfie-db-dev')


