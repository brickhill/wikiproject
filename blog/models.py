from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from blog.helpers import resize
from django.core.exceptions import ValidationError


class Series(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Series"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    def clean(self):
        super().clean()

        # Can't be your own parent
        if self.parent == self:
            raise ValidationError({
                "parent": "A category cannot be its own parent."
            })

        # Check for circular references
        parent = self.parent
        while parent:
            if parent == self:
                raise ValidationError({
                    "parent": "This would create a circular hierarchy."
                })
            parent = parent.parent

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    excerpt = models.TextField(blank=True)

    categories = models.ManyToManyField(Category, blank=True)
    # series = models.ManyToManyField(Series, through="SeriesPost", blank=True)

    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True
    )
    allow_comments = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        resize(self.image, width=250)

    def __str__(self):
        return self.title


class Page(models.Model):
    KEYWORD_CHOICES = [
        ('home', 'Home Page'),
        ('terms', 'Terms & Conditions'),
        ('privacy', 'Privacy'),
        ('cookie', 'Cookie Policy')
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = RichTextUploadingField()
    keyword = models.CharField(
        max_length=7,
        choices=KEYWORD_CHOICES,
        null=True,
        blank=True,
        unique=True,
        help_text="Keyword"
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        resize(self.image, width=250)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Comment by {self.user}'


class SeriesPost(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Series/Post'
        ordering = ['order']

    def __str__(self):
        return f"{self.series}/{self.post}"
