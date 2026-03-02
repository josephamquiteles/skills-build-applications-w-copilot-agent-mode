
from django.core.management.base import BaseCommand
from pymongo import MongoClient
from bson.objectid import ObjectId

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        # Collections
        users = db['users']
        teams = db['teams']
        activities = db['activities']
        leaderboard = db['leaderboard']
        workouts = db['workouts']

        # Clear existing data
        users.delete_many({})
        teams.delete_many({})
        activities.delete_many({})
        leaderboard.delete_many({})
        workouts.delete_many({})

        # Teams
        marvel_id = ObjectId()
        dc_id = ObjectId()
        teams.insert_many([
            {'_id': marvel_id, 'name': 'Team Marvel'},
            {'_id': dc_id, 'name': 'Team DC'}
        ])

        # Users
        user_data = [
            {'_id': ObjectId(), 'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team_id': marvel_id},
            {'_id': ObjectId(), 'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_id},
            {'_id': ObjectId(), 'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_id},
            {'_id': ObjectId(), 'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_id},
        ]
        users.insert_many(user_data)

        # Activities
        activities.insert_many([
            {'user_email': 'spiderman@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user_email': 'ironman@marvel.com', 'activity': 'Cycling', 'duration': 45},
            {'user_email': 'wonderwoman@dc.com', 'activity': 'Swimming', 'duration': 60},
            {'user_email': 'batman@dc.com', 'activity': 'Yoga', 'duration': 40},
        ])

        # Workouts
        workouts.insert_many([
            {'name': 'Full Body Blast', 'suggested_for': 'marvel'},
            {'name': 'Hero Strength', 'suggested_for': 'dc'},
        ])

        # Leaderboard
        leaderboard.insert_many([
            {'team': 'Team Marvel', 'points': 75},
            {'team': 'Team DC', 'points': 100},
        ])

        # Ensure unique index on email
        users.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
