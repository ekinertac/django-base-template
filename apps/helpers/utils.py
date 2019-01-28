import datetime
import os


def upload_path(instance, filename):
    """
    Set uploaded image's path

    :param <str> filename:
    :param <cls> instance:
    :return: <str> /instance_name/2015/05/12/filename.jpg
    """
    now = datetime.datetime.now()
    return os.path.join(
        instance.__class__.__name__.lower(),
        "%s" % now.strftime('%Y'),
        "%s" % now.strftime('%m'),
        "%s" % now.strftime('%d'),
        filename
    )


def get_object_or_false(model, **kwargs):
    # Exception handler, if given filter does not exists return false
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return False


def has_field(model, fieldname):
    # Checks model has given field
    for field in model._meta.fields:
        if field.__class__.__name__ == fieldname:
            return True
    return False
