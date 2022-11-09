# Webhook for WhatsApp automation

A webhook in Python Django framework for WhatsApp automation. This project is developed
using [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api).

---


## Prerequisite

- Python3
- Django
- JSON

## Installation

### Setup firebase

1. Create new project in firebase
2. Setup realtime database
3. Navigate to Project Settings > Service Accounts > Firebase Admin SDK
4. Select Python Language then generate new private key, This will download json file.
5. Now copy the content of this JSON file and paste it in `webhook/firebase.py` (Line 10-21).
6. Then copy the database URL from Realtime Database Firebase Console and paste it in `webhook/firebase.py` (Line 8).

### Project Setup

1. Clone this repository to your workspace

```shell
git clone https://github.com/parth-p-7span/wabot-django.git
```

2. Navigate to wabot-django directory in your terminal

```shell
cd wabot-django
```

3. Install required packages using below command

```shell
pip install -r requirements.txt
```

4. Add your database in `wabot/settings.py` file
5. Migrate database with following commands

```shell
python manage.py makemigrations
python manage.py migrate
```

6. Run the project using below command

```shell
python manage.py runserver
```

### Webhook Setup

1. Deploy the project in any platform and obtain endpoint URL.
    - [Hosting a Django Project on Heroku](https://realpython.com/django-hosting-on-heroku/)
    - [Hosting a Django Project on PythonAnywhere](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
2. Configure webhook in Meta developer
   portal. (
   Please [read this]((https://developers.facebook.com/docs/graph-api/webhooks/getting-started#configure-webhooks-product))
   before proceeding ahead)
3. Verify Token is given in the `wabot/settings.py` file with name `WA_VERIFY_TOKEN`

---

## Important Files

- `webhook/actions.json` : A JSON file that holds all the actions needed to perform by the bot.
- `webhook/firebase.py` : A Python file for connecting app to firebase and performing actions.
- `webhook/func.py` : A Python file for performing whatsapp actions like send message, mark as read message, and send
  input validation error message.
- `webhook/input_validator.py` : This file contains all the functions for validating input messages.

---

## `actions.json` structure

- The primary key of object contains the order of message that has to be sent via BOT.
- `next` key has the data of next message after performing one action.
- `type` key has the data type of Bot's message
- `user_input` key has boolean value. If it is true, the bot will wait for the user to send a message before sending the
  subsequent message; otherwise, the bot will keep sending subsequent messages.
- `expected` key has the expected type of user's message. A validation error is sent if the user submits a message with
  the incorrect message type.
- `child` key has the data of the message body as
  per [Whatsapp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api/).
