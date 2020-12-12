from django.contrib import admin
from .models import Post, Comment, Message
from django_summernote.admin import SummernoteModelAdmin

# @admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'author', 'updated_on', 'created_on', 'language', 'status')
    list_filter = ("status","language")
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Post, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'body')
    # actions = ['remove_comments']

    # def remove_comments(self, request, queryset):
    #     queryset.update(active=False)



class MessageAdmin(admin.ModelAdmin):
    summernote_fields = ('content',)
    list_display = ('email','subject', 'user_to_reply','created_on', 'is_replied', 'is_read')
    list_filter = ('created_on', 'is_replied','user_to_reply', 'is_read')

admin.site.register(Message, MessageAdmin)


# class MailAdmin(admin.ModelAdmin):
#     summernote_fields = ('content',)
#     list_display = ('message', 'subject', 'created_on')
#     list_filter = ('created_on',)

# admin.site.register(Mail, MailAdmin)