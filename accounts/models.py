from django.contrib.auth.models import User
from django.db import models

class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follow {}'.format(self.user_from, self.user_to)

# User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))
