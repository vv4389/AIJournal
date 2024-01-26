import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Replace with your actual client secret data
CLIENT_SECRET_DATA = {
    "web": {
        "client_id": "7516259251-matcccb0og6k3mku0nm882toj8n2rmtc.apps.googleusercontent.com",
        "project_id": "ai-journal-412319",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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"
    }
}

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def authenticate(client_secret_data, token_path):
    credentials = None

    if os.path.exists(token_path):
        credentials = Credentials.from_authorized_user_file(token_path)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(client_secret_data, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(credentials.to_json())

    return credentials

def search_media_items(credentials):
    import requests

    headers = {
        'Authorization': f'Bearer {credentials.token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'filters': {
            'dateFilter': {
                'ranges': [
                    {
                        'startDate': {
                            'day': 1,
                            'month': 1,
                            'year': 2024,
                        },
                        'endDate': {
                            'day': 15,
                            'month': 1,
                            'year': 2024,
                        },
                    },
                ],
            },
            'contentFilter': {
                'includedContentCategories': [
                    'PEOPLE',
                    'SELFIES',
                ],
            },
            'mediaTypeFilter': {
                'mediaTypes': [
                    'PHOTO',
                ],
            },
        },
    }

    response = requests.post(
        'https://photoslibrary.googleapis.com/v1/mediaItems:search?key=AIzaSyAGQjDk_YJywo3mcL5ZsklXEr3nCat1FtQ',
        headers=headers,
        json=json_data,
    )
    # Decode bytes to string
    response_string = response.content.decode('utf-8')

    # Load the JSON string
    response_json = json.loads(response_string)

    # Pretty print the JSON
    formatted_json = json.dumps(response_json, indent=2)

    print(formatted_json)
    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    # data = '{"filters":{"dateFilter":{"ranges":[{"startDate":{"day":1,"month":1,"year":2024},"endDate":{"day":15,"month":1,"year":2024}}]},"contentFilter":{"includedContentCategories":["PEOPLE","SELFIES"]},"mediaTypeFilter":{"mediaTypes":["PHOTO"]}}}'
    # response = requests.post(
    #    'https://photoslibrary.googleapis.com/v1/mediaItems:search?key=[YOUR_API_KEY]',
    #    headers=headers,
    #    data=data,
    # )
    # service = build('photoslibrary', 'v1', credentials=credentials)
    #
    # request_body = {
    #     "filters": {
    #         "dateFilter": {
    #             "ranges": [
    #                 {
    #                     "startDate": {"day": 1, "month": 1, "year": 2024},
    #                     "endDate": {"day": 15, "month": 1, "year": 2024}
    #                 }
    #             ]
    #         },
    #         "contentFilter": {"includedContentCategories": ["PEOPLE", "SELFIES"]},
    #         "mediaTypeFilter": {"mediaTypes": ["PHOTO"]}
    #     }
    # }
    #
    # response = service.mediaItems().search(body=request_body).execute()
    # return response

def main():
    token_path = 'token.json'  # Replace with your actual token file path

    credentials = authenticate(CLIENT_SECRET_DATA, token_path)

    result = search_media_items(credentials)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
