import firebase_admin
from firebase_admin import db
import json


class Firebase:
    def __init__(self):
        database_url = "https://wa-bot-4eb4a-default-rtdb.asia-southeast1.firebasedatabase.app/"
        cred_obj = firebase_admin.credentials.Certificate(
            {
                "type": "service_account",
                "project_id": "wa-bot-4eb4a",
                "private_key_id": "96dbd6de2bd2088ed1949f22858aa88bdb3d1624",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDE409xdXysb4lR\n7yWnKh1dZaScAX5YtalLjma95jRiiuL7a8PLKguTivEt8b7e6hNmJ/FYgs7wGrdW\nfVjqCHAmaoH/NzfKejehPawRCIVg2PQ2fCt7m+1qh1AyUcpHawXcKboLJVXQZTG/\nT5Vdrrs9HChHlx4GOf2aVmmbIEfJrpJctDZRC2TaSVf8Q5BtpQQNyLA0VDYzVOBX\n30ExEHM/e7KWMQSslYBIjw2IqiXGlqjpmLuIeryCw9KWSStn8fpoVxl9E3SP4KJU\ntXm/tT6sCNj8uzGEANcSrnr2h51EqpA4Ht7lRY1zulRSC4IQc6Gbfh6oKZSmwHBV\nzPADQbAXAgMBAAECggEADL4Paq7pYjmXwBNDsxVxMBW/eQ9Jr5EWQ1sUgC7Rbh1C\nAnafhdsTQ7nG0SvnqAKrPb3RC2Lv5K899V2IbyEbrQjQoAVhWXvedNOKetG73CA+\ncfZIVCgrzeyy/oa3mjateunCbi086A9ckF6kspr36EUVwEhh+5IuPRphnFYS/1Tt\nVET3u8rkBDawiRAUz+whMn7X3fmA5pqBgN1izMck6RVgddq6glNTazcDSsU/Gy63\n5OQpNlNFxgahu3GwxDAbUjqYd/kkPUq7WuQ/FOkZp2nwa/yFOH0K5cgX3NomJTcE\nc6+gSrlfAp2avKGYzKkMw3ngXJbGRuRbhXRy/ccBeQKBgQD4Ke+4CRMkWMF+CkLO\nb7XLTe0MSEDmuz22m3cu05UOWQ8mFrTDVsBVstAMtYvO5qG2efeH0AlA50cZoL1C\nIsmS/GBlW7PknPNPaPqMCbAIiXAN6xPv7qDopclqpzv04mUTfBgqlb1RYRPQI1Ip\njvw/A4CJ77Wn0yrvJGJoVN6AGQKBgQDLGuD7LBPoFACUGSMEcZR/1107o1L2nlyg\nV+Ppjfs/OWVslfycSdyqehO2Y3zdQwL5pFjrYneSpTXRnCn4jCyg3ELUsDL5/5qB\nsHRYBMYisx0agIApxcOtMO6ALtLDyzDGarjQ9Wkq144UwEhVUk6mQFCj/iAouEPJ\nsSGX0BD3rwKBgQCF22j4ZbyzgERuTe6XF16B2PiiBV8slZbGJrl0wp/F63fmXZ0H\nOIXqM9dQ46QT6AcWPFeuJCK5pYaOZktvnwAHjqYYRgyUpawAC2oJmzgegrO0bjaE\n1rxogPRR2P7YKj3G8sq+PaKugKSFQmgRDpU1EBiHTos3iQnBkGicShryEQKBgB0v\nIo7U2ZNqdF7TcdWsoGLyRkJQiJZJURP1LRmdPjHqhGli7+ZhMqUIX5bAmuuMOnw2\nolRIVNgshxw0bU96jNscazn2i4yirsfd3Andvb60sATj3AaklSZotoySrdRWeQ65\nvQ7BhLgUOyU+L+aaqhR3f17hICvZtlvf6OzQh++fAoGAD0sNPY7cF1WZukYqxcL8\nHAX+8HFNzHIGhCkVkuWwpBfIzMszo6sXnPEGLS3DNV7a3qcLAnq8RJFBeyTZDu5a\ncOtjfu5ffGGPGUjD72w/LkO5d0kEz9IbymFB67awVht8hsLco6o/5xHS+m1jmeY1\nhupCn4O8azKpZTHEs64j8To=\n-----END PRIVATE KEY-----\n",
                "client_email": "firebase-adminsdk-foyvr@wa-bot-4eb4a.iam.gserviceaccount.com",
                "client_id": "106928262711341906932",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-foyvr%40wa-bot-4eb4a.iam.gserviceaccount.com"
            }
        )
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
