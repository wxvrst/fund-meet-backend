from django.contrib import admin

from content.models import PublicationModel, PublicationTagModel, PublicationCommentModel, PublicationContentModel


@admin.register(PublicationModel)
class PublicationModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'author')
    search_fields = ('header', 'author', 'tags')
    list_filter = ('author', 'tags')

admin.site.register(PublicationTagModel)
admin.site.register(PublicationContentModel)

@admin.register(PublicationCommentModel)
class PublicationCommentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor',)
    search_fields = ('autor',)
    list_filter = ('autor',)
