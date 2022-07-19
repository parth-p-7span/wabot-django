import firebase_admin
from firebase_admin import db
import json


class Firebase:
    def __init__(self):
        database_url = "https://wa-bot-4eb4a-default-rtdb.asia-southeast1.firebasedatabase.app/"
        cred_obj = firebase_admin.credentials.Certificate(
            './webhook/wa-bot-4eb4a-firebase-adminsdk-foyvr-96dbd6de2b.json')
        default_app = firebase_admin.initialize_app(cred_obj, {
            'databaseURL': database_url
        })

    @staticmethod
    def create_user(user_id, whatsapp_name):
        ref = db.reference('/')
        ref.update({user_id: {'wa_name': whatsapp_name}})
        return ref.get()

    @staticmethod
    def update_user(user_id, field_name, field_value):
        ref = db.reference(f'/{user_id}')
        ref.update({field_name: field_value})
        return ref.get()

    @staticmethod
    def get_user_data(user_id):
        with open('webhook/actions.json', 'r') as f:
            actions = json.load(f)

        actions_array = {}
        for a in actions['steps']:
            actions_array[a['name']] = 0

        ref = db.reference(f'/{user_id}/state')
        data = ref.get()

        if isinstance(data, dict):
            for key in data.keys():
                actions_array[key] = 1

        return actions_array

    @staticmethod
    def delete_data(user_id):
        ref = db.reference(f'/{user_id}')
        res = ref.delete()
        return res

    @staticmethod
    def update_state(user_id, state, action_type):
        ref = db.reference(f'/{user_id}/state')
        res = ref.update({'state': state, 'action_type': action_type})
        return res

    @staticmethod
    def get_state(user_id):
        ref = db.reference(f'/{user_id}/state')
        return ref.get()
