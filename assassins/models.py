from django.db import models
from django.utils.timezone import utc
import datetime


class Player(models.Model):
    sunetid = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    target = models.OneToOneField('self', null=True, blank=True)
    assign_time = models.DateTimeField(null=True, blank=True)
    living = models.BooleanField(default=True)

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def kill_target(self, details):
        victim = self.target
        self.target = victim.target
        victim.die()
        self.assign_time = datetime.datetime.now().replace(tzinfo=utc)
        self.save()

    def die(self):
        self.target = None
        self.living = False
        self.save()


class Quote(models.Model):
    text = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    source = models.CharField(max_length=200)

    def __unicode__(self):
        return self.text
