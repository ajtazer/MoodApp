"""Minimal Vercel Blob client (the REST call the official SDKs make)."""
import os

import requests

API_URL = "https://blob.vercel-storage.com"


class BlobError(Exception):
    pass


def put_blob(pathname, data, content_type):
    """Upload bytes or a file object as a public blob and return its URL."""
    token = os.environ.get("BLOB_READ_WRITE_TOKEN")
    if not token:
        raise BlobError("BLOB_READ_WRITE_TOKEN is not set")
    response = requests.put(
        f"{API_URL}/{pathname}",
        data=data,
        headers={
            "authorization": f"Bearer {token}",
            "x-api-version": "7",
            "access": "public",
            "x-content-type": content_type or "application/octet-stream",
        },
        timeout=60,
    )
    if response.status_code not in (200, 201):
        raise BlobError(f"{response.status_code}: {response.text[:300]}")
    return response.json()["url"]
