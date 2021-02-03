"""Module for generating events by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Event
from levelupreports.views.connection import Connection

def userevent_list(request):
    """Function to build an HTML report of events by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn: 
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games with related user info.
            db_cursor.execute("""
            SELECT
                id,
                description,
                date,
                time,
                title,
                user_id,
                full_name
            FROM
                EVENTS_BY_USER

            """)

            dataset = db_cursor.fetchall()

#             {
#     1: {
#         "gamer_id": 1,
#         "full_name": "Molly Ringwald",
#         "events": [
#             {
#                 "id": 5,
#                 "date": "2020-12-23",
#                 "time": "19:00",
#                 "game_name": "Fortress America"
#             }
#         ]
#     }
# }

            events_by_user = {}

            for row in dataset:
                # Create a Game instance and set its properties
                event = Event()
                event.date = row["date"]
                event.time = row["time"]
            

                # Store the user's id
                uid = row["user_id"]

                #if the user's id is already a key in the dictionary ...
                if uid in games_by_user:

                    # Add the current game to the 'games' list for it
                    events_by_user[uid]['events'].append(event)

                else:
                    # Otherwise, create the key and dictionary value
                    events_by_user[uid] = {}
                    events_by_user[uid]["id"] = uid
                    events_by_user[uid]["full_name"] = row["full_name"]
                    events_by_user[uid]["events"] = [event]

        # Get only the values from the dictionary and create a list from them
        list_of_users_with_events = events_by_user.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_events.html'
        context = {
            'userevent_list': list_of_users_with_events
        }       

        return render(request, template, context)
