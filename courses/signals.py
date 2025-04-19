# from pyfcm import FCMNotification
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Course

# push_service = FCMNotification(api_key='YOUR_FCM_SERVER_KEY')

# @receiver(post_save, sender=Course)
# def send_course_notification(sender, instance, created, **kwargs):
#     if created:
#         result = push_service.notify_topic_subscribers(
#             topic_name='new_courses',
#             message_title='New Course Added',
#             message_body=f'A new course "{instance.title}" has been added!',
#             data_message={
#                 'course_id': str(instance.id),
#                 'course_title': instance.title,
#             }
#         )
#         print(result)