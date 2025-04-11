from django.core.files.storage import Storage
from django.conf import settings
from django.utils.deconstruct import deconstructible
import os
from urllib.parse import urljoin
import requests
from django.core.files.base import ContentFile
import json

@deconstructible
class VercelBlobStorage(Storage):
    def __init__(self):
        self.client_token = os.environ.get('BLOB_READ_WRITE_TOKEN')
        self.base_url = "https://3rm9kzfdjv9bixty.public.blob.vercel-storage.com"
        self.api_url = "https://blob.vercel-storage.com"

    def _save(self, name, content):
        # Get upload URL from Vercel Blob
        headers = {
            'Authorization': f'Bearer {self.client_token}',
            'Content-Type': 'application/json'
        }
        
        # Get upload URL
        response = requests.post(
            f"{self.api_url}/upload",
            headers=headers,
            json={
                'contentType': content.content_type,
                'pathname': f'media/{name}'
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get upload URL: {response.text}")
        
        upload_data = response.json()
        
        # Upload file to Vercel Blob
        with content.file.open('rb') as file:
            upload_response = requests.put(
                upload_data['uploadUrl'],
                data=file,
                headers={'Content-Type': content.content_type}
            )
            
        if upload_response.status_code not in [200, 201]:
            raise Exception(f"Failed to upload file: {upload_response.text}")
            
        return name

    def url(self, name):
        return f"{self.base_url}/media/{name}"

    def exists(self, name):
        try:
            response = requests.head(self.url(name))
            return response.status_code == 200
        except:
            return False

    def delete(self, name):
        # Implement if needed
        pass

    def listdir(self, path):
        # Implement if needed
        return [], [] 