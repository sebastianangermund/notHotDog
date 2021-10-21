import os
import uuid
import pika
import json

import tensorflow as tf
tf.compat.v1.disable_eager_execution() # quick fix for tf v2 compatability

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.reverse import reverse as api_reverse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Photo(models.Model):
    """Model representing a specific picture."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    uploaded = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d',
        height_field=None,
        width_field=None,
        max_length=100,
        null=True,
    )
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=160, blank=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    flagged = models.BooleanField(default=False)

    class Meta:
        ordering = ['uploaded', 'owner']

    def __str__(self):
        return f'{self.owner} ({self.uploaded})'

    def get_absolute_url(self):
        return reverse('my-photo-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)


@receiver(post_save, sender=Photo)
def analyze_Photo(created, instance, **kwargs):
    """This function sometimes creates a task that is queued in RabbitMQ.

    When a photo instance is created:
        Analyze the photo.
    When a photo instance is changed:
        Do nothing if it's flagged (would create infinite loop)
        Else analyze the photo

    Remember to take care of the queued objects! Do this by
    running photo_consumer.py which is located at root_dir/classifier.

    """

    if ((not instance.flagged) or created):
        try:
            file_name = os.path.join(BASE_DIR, instance.photo.path)
            print(file_name)
        except ValueError:
            print('Photo not registered. If You\'re testing, all is good.')
        else:
            array_file = read_tensor_from_image_file(file_name)
            if array_file == 'NOT_SUPPORTED':
                print('This format is not supported')
                return

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'),
            )
            channel = connection.channel()
            channel.queue_declare(queue='new_task')

            username = str(instance.owner)
            password = instance.owner.password

            instanceURL = api_reverse('photo-detail', kwargs={'pk': instance.pk})
            rawMessage = {
                'photo': array_file.tolist(),
                'url': instanceURL,
                'flag': instance.flagged
            }
            message = json.dumps(rawMessage)

            channel.basic_publish(
                exchange='',
                routing_key='new_task',
                body=message,
            )
            connection.close()


def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
    input_name = "file_reader"
    file_reader = tf.io.read_file(file_name, input_name)
    if file_name.endswith(".png"):
        image_reader = tf.image.decode_png(
            file_reader, channels=3, name="png_reader")
    elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(
            tf.image.decode_gif(file_reader, name="gif_reader"))
    elif file_name.endswith(".bmp"):
        image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
    elif file_name.endswith(".jpg") or file_name.endswith(".jpeg"):
        image_reader = tf.image.decode_jpeg(
            file_reader, channels=3, name="jpeg_reader")
    else:
        return 'NOT_SUPPORTED'
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize(
        dims_expander,
        [input_height, input_width]
    )
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    with tf.compat.v1.Session() as sess:
        return sess.run(normalized)
