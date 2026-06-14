from django.db import models

class PublicationModel(models.Model):
    header = models.CharField(max_length=255, null=False, blank=False)

    author = models.ForeignKey(
        'core.UserModel',
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name='publications'
    )

    tags = models.ManyToManyField(to="PublicationTagModel", verbose_name="Теги", related_name="publications", blank=True)

    likes_count = models.IntegerField(default=0, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ['date_added']


class PublicationContentModel(models.Model):
    publication = models.ForeignKey(
        PublicationModel,
        on_delete=models.CASCADE,
        verbose_name="Публикация",
        related_name='content',
        null=True, blank=True,
    )

    text_content = models.TextField(null=True, blank=True)
    image_content = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"


class PublicationTagModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class PublicationCommentModel(models.Model):
    author = models.ForeignKey('core.UserModel', on_delete=models.CASCADE, verbose_name="Автор", related_name='comments')
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name="Родительский коммент",
        related_name='response',
        null=True, blank=True,
    )
    publication = models.ForeignKey(
        PublicationModel,
        on_delete=models.CASCADE,
        verbose_name="Публикация",
        related_name='comments',
        null=True, blank=True,
    )

    text = models.TextField(null=False, blank=False)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.author)} {str(self.date_added)} {'response to ' + str(self.parent_comment) if self.parent_comment else ''}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


