import datetime

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django_extensions.db.fields import AutoSlugField
from sorl.thumbnail import ImageField

from apps.helpers.utils import upload_path


class BaseModel(models.Model):

    def update(self, *args, **kwargs):
        not_allowed_fields = ['id', 'pk']
        for field in not_allowed_fields:
            if kwargs.get(field, False):
                kwargs.pop(field)

        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise FieldDoesNotExist("{} model has no field '{}'".format(self._meta.verbose_name, key))
        self.save()
        return self

    class Meta:
        abstract = True


class GenericModelMixin(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()

    class Meta:
        abstract = True


class UserMixin(models.Model):
    user = models.ForeignKey(get_user_model(), blank=True, null=True)

    class Meta:
        abstract = True


class TitleMixin(models.Model):
    title = models.CharField(u"Title", max_length=512)
    slug = AutoSlugField(
        verbose_name=u'Slug',
        unique=True,
        populate_from=['title', 'id']
    )

    def __unicode__(self):
        return u"%s" % self.title

    class Meta:
        abstract = True


class TimeFrameMixin(models.Model):
    """
    An abstract base class model that provides ``start``
    and ``end`` fields to record a timeframe.
    """
    started_at = models.DateTimeField(u"Starting at", default=datetime.datetime.now)
    ended_at = models.DateTimeField(u"Ending at", default=datetime.datetime.now)

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    """
    An abstract base class that provides self-updated `created` and `modified` options.
    """
    def created(self):
        if self.pk:
            entry = LogEntry.objects.get(
                content_type_id=ContentType.objects.get_for_model(self).pk,
                object_id=self.pk, action_flag=ADDITION
            )
            return entry
        else:
            return False

    def modified(self):
        if self.pk:
            try:
                entry = LogEntry.objects.filter(
                    content_type_id=ContentType.objects.get_for_model(self).pk,
                    object_id=self.pk, action_flag=CHANGE
                ).order_by('-action_time')[0]
                return entry
            except IndexError:
                pass
        return None

    def created_at(self):
        created = self.created()
        return created.action_time if created else None

    def created_by(self):
        created = self.created()
        return created.user if created else None

    def modified_at(self):
        modified = self.modified()
        return modified.action_time if modified else None

    def modified_by(self):
        modified = self.modified()
        return modified.user if modified else None

    class Meta:
        abstract = True


class OrderMixin(models.Model):
    order = models.PositiveIntegerField(u"Order", default=0)

    class Meta:
        abstract = True
        ordering = ['order', ]


class ImageMixin(models.Model):
    image = ImageField(upload_to=upload_path, blank=True, null=True)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return None

    class Meta:
        abstract = True
