# Vercel Deployment Guide

This guide will help you set up your MoodNotes application for deployment on Vercel with Cloudflare D1 database and Vercel Blob Storage.

## Prerequisites

1. A Vercel account
2. Vercel CLI installed (optional, for local testing)
3. Cloudflare D1 database created
4. A Cloudflare API token with D1 access created
5. Vercel Blob Storage configured

## Environment Variables

Set up the following environment variables in your Vercel project settings:

### Cloudflare D1 Configuration
- `CLOUDFLARE_D1_DATABASE_ID` - Your D1 database ID
- `CLOUDFLARE_ACCOUNT_ID` - Your Cloudflare Account ID
- `CLOUDFLARE_D1_API_TOKEN` - Your Cloudflare API Token with D1 permissions

### Vercel Blob Storage Configuration
- `VERCEL_BLOB_ACCESS_KEY_ID` - Your Vercel Blob Storage access key ID
- `VERCEL_BLOB_SECRET_ACCESS_KEY` - Your Vercel Blob Storage secret access key
- `VERCEL_BLOB_BUCKET_NAME` - Your Vercel Blob Storage bucket name
- `VERCEL_BLOB_ENDPOINT_URL` - Your Vercel Blob Storage endpoint URL
- `VERCEL_BLOB_MEDIA_URL` (optional) - Custom URL for media files

### Other Settings
- `DEBUG_FLAG` - Set to 'False' for production
- `VERCEL` - Should be automatically set to '1' by Vercel

## Deployment Steps

1. Connect your GitHub repository to Vercel
2. Configure the environment variables listed above
3. Deploy your application

## Local Development

For local development, the application will use:
- SQLite database (db.sqlite3)
- Local media storage (/media/)

To run locally:
```bash
# Install dependencies if needed
# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt

python3 manage.py migrate
python3 manage.py runserver
```

## Troubleshooting

### Media Files Not Appearing
- Check that your Vercel Blob Storage credentials are correct
- Verify that the `VERCEL_BLOB_ENDPOINT_URL` is correctly formatted
- Ensure `DEFAULT_FILE_STORAGE` is properly configured

### Database Connection Issues (Cloudflare D1)
- Verify Cloudflare D1 credentials (`DATABASE_ID`, `ACCOUNT_ID`, `API_TOKEN`)
- Ensure the API token has the correct permissions for the D1 database.
- Check Vercel deployment logs for specific D1 connection errors.
- Ensure your D1 database is properly initialized with migrations (Vercel build process handles this).

### Static Files Issues
- Run `python3 manage.py collectstatic` locally to check for errors
- Verify the paths in vercel.json 