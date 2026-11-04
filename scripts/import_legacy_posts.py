"""Bring the two posts made on the old local database into the live feed.

Idempotent: a post whose original id already exists is skipped, so running it on
every build is safe. Images are re-encoded without EXIF metadata (phone photos can
carry GPS location) and uploaded to Vercel Blob. Likes and the comment are only
added when those users exist in this database.
Run with: python manage.py shell < scripts/import_legacy_posts.py
"""
import io
import os
import uuid
from datetime import datetime, timezone

from django.contrib.auth.models import User
from PIL import Image, ImageOps

from MoodApp.blob import put_blob
from social.models import Comment, Post

HERE = os.path.join(os.getcwd(), 'scripts', 'legacy_posts')

LEGACY = [
    {
        'id': '64392a9d-cbce-4fe5-bb10-092862f66c88',
        'user': 'oho',
        'caption': 'imma baddie',
        'created': datetime(2025, 4, 7, 15, 7, 42, tzinfo=timezone.utc),
        'file': 'imma-baddie.jpg',
        'liked_by': ['oho'],
        'comments': [('oho', 'bwahaha kyutt', datetime(2025, 4, 7, 15, 25, 41, tzinfo=timezone.utc))],
    },
    {
        'id': 'dde419bd-3c31-49d6-9ab7-8fcf1884b643',
        'user': '12312',
        'caption': 'lets upload this abhay',
        'created': datetime(2025, 4, 11, 21, 40, 16, tzinfo=timezone.utc),
        'file': 'lets-upload-this-abhay.jpeg',
        'liked_by': ['12312'],
        'comments': [],
    },
]


def clean_jpeg(path):
    """Re-encode without EXIF (location etc.), keeping the right orientation."""
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img).convert('RGB')
        out = io.BytesIO()
        img.save(out, format='JPEG', quality=88)
        return out.getvalue()


for item in LEGACY:
    if Post.objects.filter(id=item['id']).exists():
        print(f"legacy posts: '{item['caption']}' already imported")
        continue
    url = put_blob(f"posts/legacy-{uuid.uuid4().hex[:8]}-{item['file']}", clean_jpeg(os.path.join(HERE, item['file'])), 'image/jpeg')
    post = Post.objects.create(id=item['id'], user=item['user'], caption=item['caption'], created=item['created'], image=url)
    likers = list(User.objects.filter(username__in=item['liked_by']))
    if likers:
        post.liked_by.add(*likers)
        post.likes = len(likers)
        post.save(update_fields=['likes'])
    for username, text, created in item['comments']:
        author = User.objects.filter(username=username).first()
        if author:
            Comment.objects.create(post=post, user=author, text=text, created=created)
    print(f"legacy posts: imported '{item['caption']}' ({len(likers)} like(s))")
