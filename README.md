# Performing Arts Alumni Society

## Version 0.3.0

Django-based Website

[Release Notes](RELEASE_NOTES.md)

## Deploy Instructions

1. Configure `.env`:
    ```
    # required
    SECRET_KEY
    ALLOWED_HOSTS

    # recommended
    TIME_ZONE

    # database
    DB_NAME
    DB_USER
    DB_PASS
    ```

2. Run commands:
    ```
    python manage.py migrate
    python manage.py collectstatic -i sass --noinput
    python manage.py compress --force
    ```
