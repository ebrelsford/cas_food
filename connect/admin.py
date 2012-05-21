from django.contrib import admin

from models import Video, TwitterFeed

class VideoAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text',)
    list_display = ('title', 'text',)

class TwitterFeedAdmin(admin.ModelAdmin):
    search_fields = ('handle', 'text',)
    list_display = ('handle', 'text',)

admin.site.register(Video, VideoAdmin)
admin.site.register(TwitterFeed, TwitterFeedAdmin)
