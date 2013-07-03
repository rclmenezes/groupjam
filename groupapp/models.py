from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from groupapp.croppable.fields import CroppableImageField
from groupapp.croppable.utils import get_crop_processor
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToCover

# used for S3 path
def s3_path_name(instance, filename):
    extension = filename.rsplit('.', 1)[1]
    rand = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
    return 'person/' + str(instance.id) + "/" + rand +  "." + extension

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    picture = CroppableImageField(invalidate_on_save=['picture_cropped'], upload_to=s3_path_name, blank=True)
    picture_cropped = ImageSpecField(get_crop_processor(image_field='picture', after_processors=[ResizeToFill(80, 80)]), image_field='picture')
    picture_profile = ImageSpecField([ResizeToCover(140, 300)], image_field='picture')

class Group(models.Model):
    PUBLIC = 'PU'
    PRIVATE = 'PR'
    PRIVACY_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private')
    )

    ADMIN_INVITE = 'AD'
    MEMBER_INVITE = 'ME'
    ANYONE_INVITE = 'AN'
    JOINING_CHOICES = (
        (ADMIN_INVITE, 'Invite through admins'),
        (MEMBER_INVITE, 'Invite through members'),
        (ANYONE_INVITE, 'Anyone can join')
    )

    creator = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=40)
    url = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now=True)
    privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES)
    joining = models.CharField(max_length=2, choices=JOINING_CHOICES)

class UserGroup(models.Model):
    user = models.ForeignKey(UserProfile)
    group = models.ForeignKey(Group)
    allow_email = models.BooleanField(default=True)
    is_administrator = models.BooleanField(default=False)

class Thread(models.Model):
    creator = models.ForeignKey(UserProfile)
    subject = models.CharField(max_length=200)
    text = models.TextField()
    group = models.ForeignKey(Group)
    created_at = models.DateTimeField(auto_now=True)

class Post(models.Model):
    creator = models.ForeignKey(UserProfile)
    thread = models.ForeignKey(Thread)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
    creator = models.ForeignKey(UserProfile)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    like_object = generic.GenericForeignKey('content_type', 'object_id')

class Follow(models.Model):
    creator = models.ForeignKey(UserProfile)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    like_object = generic.GenericForeignKey('content_type', 'object_id')

