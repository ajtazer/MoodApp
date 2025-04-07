# MoodNotes

MoodNotes is a Python Django web application that allows users to express and share their mood through written notes.
# [Click to View](https://themoodapp.vercel.app/)

## Features

* User registration and login
* Secure authentication and password management
* Capturing and storing mood-related notes
* Planned features include note creation, editing, and deletion, tags and categories, user profiles, and social sharing options

## Technologies

* Python Django Framework
* HTML/CSS
* JavaScript (for frontend interactivity)
* PostgreSQL (production database)

## Prerequisites

1. A Vercel account
2. Vercel CLI installed (optional, for local testing)
3. Vercel Postgres database configured
4. Vercel Blob Storage configured

## Environment Variables

Set up the following environment variables in your Vercel project settings:

### Vercel Postgres Configuration
- `POSTGRES_DATABASE` - Your Postgres database name
- `POSTGRES_USER` - Your Postgres username
- `POSTGRES_PASSWORD` - Your Postgres password
- `POSTGRES_HOST` - Your Postgres host

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

1. Connect your GitHub repository to Vercel.
2. Configure the environment variables listed above.
3. Deploy your application.

## Local Development

For local development, the application will use:
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
- Check that your Vercel Blob Storage credentials are correct.
- Verify that the `VERCEL_BLOB_ENDPOINT_URL` is correctly formatted.
- Ensure `DEFAULT_FILE_STORAGE` is properly configured.

### Database Connection Issues
- Verify Postgres credentials (`POSTGRES_DATABASE`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`).
- Check Vercel deployment logs for specific connection errors.

### Static Files Issues
- Run `python3 manage.py collectstatic` locally to check for errors.
- Verify the paths in `vercel.json`.

## Contributing

Contributions to MoodNotes are welcomed! If you are interested in collaborating on this project, please fork the repository and submit your pull requests with any enhancements or bug fixes. Let's work together to make MoodNotes an exceptional mood-sharing platform.

## License

The MoodNotes project is licensed under the MIT License. Feel free to use, modify, and distribute the codebase as permitted by the license.

## Roadmap

The following features are planned for future releases of MoodNotes:

* Note creation, editing, and deletion
* Tags and categories for better organization
* User profiles
* Social sharing options

We are also open to suggestions for new features. If you have any ideas, please feel free to open an issue or submit a pull request.

## Thank you for your interest in MoodNotes!

We hope you enjoy using the application. If you have any questions or feedback, please feel free to contact us.
