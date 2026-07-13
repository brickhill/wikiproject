from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from blog.helpers import resize
from django.core.exceptions import ValidationError
STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]


class Series(models.Model): 
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    priority = models.IntegerField(blank=True, null=True, db_index=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
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

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    excerpt = models.TextField(blank=True)

    categories = models.ManyToManyField(Category,
                                        blank=True,
                                        related_name="posts")
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
    image_title = models.CharField(
     max_length=100,
     null=True,
     blank=True,
     help_text="Image title"
    )
    image_alt_text = models.CharField(
     max_length=100,
     null=True,
     blank=True,
     help_text="Image alt text"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)

    def clean(self):
        super().clean()
        errors = {}
        if self.image_title and not self.image:
            errors["image_title"] = "Image title can only " + \
                                    "be entered if there is an image."

        if self.image_alt_text and not self.image:
            errors["image_alt_text"] = "Image alt text can only " + \
                                       "be entered if there is an image."
        if errors:
            raise ValidationError(errors)

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
        ('hero', 'Hero'),
        ('terms', 'Terms & Conditions'),
        ('privacy', 'Privacy'),
        ('cookie', 'Cookie Policy')
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = RichTextUploadingField()
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
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
    image_title = models.CharField(
     max_length=100,
     null=True,
     blank=True,
     help_text="Image title"
    )
    image_alt_text = models.CharField(
     max_length=100,
     null=True,
     blank=True,
     help_text="Image alt text"
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

    def clean(self):
        super().clean()
        errors = {}
        if self.image_title and not self.image:
            errors['image_title'] = "Image title can only " + \
                                    "be entered if there is an image."

        if self.image_alt_text and not self.image:
            errors["image_alt_text"] = "Image alt text can only " + \
                                       "be entered if there is an image."
        if errors:
            raise ValidationError(errors)

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
    active = models.BooleanField(default=False)

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
