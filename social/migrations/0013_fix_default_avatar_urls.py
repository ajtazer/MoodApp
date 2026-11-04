"""Point default avatars at files the app actually serves.

Default profile photos were saved as Vercel Blob URLs (…/media/naruto.jpg) or bare
file names (giyu.jpg), but those files were never uploaded to the Blob store, so
every default avatar showed as a broken image. They now live in static/avatars/.
Only those broken defaults are changed; Google photos and uploads are untouched.
"""
from django.db import migrations

BLOB_MEDIA = 'https://3rm9kzfdjv9bixty.public.blob.vercel-storage.com/media/'
AVATARS = {
    'gara.jpg', 'giyu.jpg', 'gojo.jpg', 'itachi.jpg', 'jojo.jpg', 'kakashi.jpg', 'luffy.jpg', 'madara.jpg',
    'mikato.jpg', 'mikey.jpg', 'naruto.jpg', 'nezoku.jpg', 'saitama.jpg', 'sasuke.jpg', 'sukuna.jpg',
    'tanjiro.jpg', 'zenitsu.jpg', 'zoro.jpg',
}


def fix(apps, schema_editor):
    SocialProfile = apps.get_model('social', 'SocialProfile')
    for profile in SocialProfile.objects.exclude(photo__isnull=True).exclude(photo=''):
        photo = profile.photo
        name = photo[len(BLOB_MEDIA):] if photo.startswith(BLOB_MEDIA) else photo
        if '/' in name or name.startswith('http'):
            continue  # a real URL (Google photo, upload): leave it
        profile.photo = '/static/avatars/' + (name if name in AVATARS else 'naruto.jpg')
        profile.save(update_fields=['photo'])


class Migration(migrations.Migration):
    dependencies = [('social', '0012_url_fields_for_blob_storage')]
    operations = [migrations.RunPython(fix, migrations.RunPython.noop)]
