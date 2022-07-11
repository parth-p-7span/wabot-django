import firebase_admin
from firebase_admin import db


class Firebase:
    def __init__(self):
        database_url = "https://wa-bot-4eb4a-default-rtdb.asia-southeast1.firebasedatabase.app/"
        cred_obj = firebase_admin.credentials.Certificate('wa-bot-4eb4a-firebase-adminsdk-foyvr-96dbd6de2b.json')
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
        """[name, email, mobile, skills, experience, last_company, ctc, location, summary, platform]"""
        ref = db.reference(f'/{user_id}')
        data = ref.get()
        fields = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if isinstance(data, dict):
            entered_data = data.keys()
            if "wa_name" in entered_data:
                fields[0] = 1
            if "name" in entered_data:
                fields[1] = 1
            if "email" in entered_data:
                fields[2] = 1
            if "mobile" in entered_data:
                fields[3] = 1
            if "skills" in entered_data:
                fields[4] = 1
            if "experience" in entered_data:
                fields[5] = 1
            if "last_company" in entered_data:
                fields[6] = 1
            if "ctc" in entered_data:
                fields[7] = 1
            if "location" in entered_data:
                fields[8] = 1
            if "summary" in entered_data:
                fields[9] = 1
            if "platform" in entered_data:
                fields[10] = 1
            if "resume" in entered_data:
                fields[11] = 1
        return fields

    @staticmethod
    def delete_data(user_id):
        ref = db.reference(f'/{user_id}')
        res = ref.delete()
        return res
