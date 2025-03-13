from django import template
import re

register = template.Library()

@register.filter
def youtube_id(value):
    """
    Extracts the YouTube video ID from a URL.
    """
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, value)
    return match.group(1) if match else None