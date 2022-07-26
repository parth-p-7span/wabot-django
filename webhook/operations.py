from webhook.models import *


def create_user(user_id, user_name):
    data = {"wa_name": user_name}
    u = UserData(user_id=user_id, data=data)
    u.save()
    # conv = Conversation(user_id=user_id)
    # conv.save()
    u_state = UserState(user_id=user_id)
    u_state.save()


def update_user(user_id, field_name, field_value):
    u = UserData.objects.get(user_id=user_id)
    temp = {**u.data, **{field_name: field_value}}
    u.data = temp
    u.save()


def update_state(user_id, state, action_type):
    u = UserState.objects.get(user_id=user_id)
    u.state = state
    u.action_type = action_type
    u.save()
