from rest_framework.serializers import ValidationError


required_data = ["youtube.com"]


def validate_url(url: str):
    """
    Validates if the given URL is a valid YouTube URL.

    Args:
        url (str): The URL to validate.

    Returns:
        an error message if the URL is not valid, otherwise returns True.
    """
    if not url:
        raise ValidationError("URL cannot be empty.")

    if not any(required in url for required in required_data):
        raise ValidationError("Invalid URL. The URL must contain 'youtube.com'.")
