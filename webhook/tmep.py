import json

import requests
import wabot.settings as s

#
# url = "https://graph.facebook.com/v13.0/106519662119427/media"
#
# payload = {
#     'messaging_product': 'whatsapp'
# }
#
# files = [
#     ('file', ('vepaar.jpg', open('/home/parthpanchal/Pictures/vepaar_thumbnail.png', 'rb'), 'image/png'))
# ]
# headers = {
#     'Authorization': 'Bearer EABMCARdnUF8BAPxl7TAbwaxOeXXp6iLwiM4s6OTlJqqF58CPZCsBhiW2fxsowrxo4GSwPp7meHzmmTHgOGM8fo4sWxeT0E2HaUecNejdKj45SmGOTUlETyyFHR3HwqbesZCglIFgmZAvlsZAHuy7mtx9Y2AOZClsjrMYpsM8bbW6MU755jw30AIvgXZCj9HFTGsp1sqCGIX6fM7BVakINR'
# }
#
# response = requests.request("POST", url, headers=headers, data=payload, files=files)
#
# print(response.text)

# res = requests.post(
#     s.WA_ENDPOINT,
#     headers=s.WA_HEADER,
#     data=json.dumps({
#         "messaging_product": "whatsapp",
#         "to": "918780495804",
#         "type": "image",
#         "image": {
#             "link": "https://appsumo2-cdn.appsumo.com/media/deals/images/as-web-Vepaar.png",
#             "provider": {
#                 "name": "7Span"
#             }
#         }
#     })
# )

res = requests.post(
    s.WA_ENDPOINT,
    headers=s.WA_HEADER,
    data=json.dumps({
        "messaging_product": "whatsapp",
        "to": "917227856454",
        "type": "contacts",
        "contacts": [
            {
                "name": {
                    "formatted_name": "Customer Support",
                    "first_name": "Parth"
                },
                "phones": [
                    {
                        "phone": "917227856454",
                        "type": "WORK",
                        'wa_id': "917227856454"
                    }
                ]
            }
        ]
    })
)

print(res.json())
