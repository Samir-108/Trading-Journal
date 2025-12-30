from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    if not text:
        return ""
    return mark_safe(markdown.markdown(text))

@register.filter
def youtube_embed(url):
    if not url:
        return ""
    if "youtube.com" in url:
        try:
            video_id = url.split("v=")[1]
            if "&" in video_id:
                video_id = video_id.split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        except IndexError:
            return url
    elif "youtu.be" in url:
        try:
            video_id = url.split("/")[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        except IndexError:
            return url
    return url
