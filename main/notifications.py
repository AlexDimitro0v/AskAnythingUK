from .models import Notification
from datetime import datetime
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def new_candidate_notification(feedback_request, current_site, candidate):
    if feedback_request.feedbackee.userprofile.notifications:
        html_message = render_to_string(
            'main/email-template.html',
            {
                'title': feedback_request,
                'user': feedback_request.feedbackee,
                'message': f"You have a new candidate for <strong>{feedback_request}</strong>. Click the link below to learn more.",
                'link': f"http://localhost:8000/feedback-request/?request_id={feedback_request.id}",
            }
        )
        email_subject = f'New candidate for {feedback_request}'
        to_list = feedback_request.feedbackee.email
        email = EmailMultiAlternatives(
            email_subject, '-', 'from_email', [to_list])
        email.attach_alternative(html_message, "text/html")
        email.send()

    notification = Notification(user=feedback_request.feedbackee, other_user=candidate,
                                feedback_request=feedback_request, type="Candidate")
    notification.save()


def chosen_as_feedbacker_notification(feedback_request, current_site):
    if feedback_request.feedbacker.userprofile.notifications:
        html_message = render_to_string(
            'main/email-template.html',
            {
                'title': feedback_request,
                'user': feedback_request.feedbacker,
                'message': f"Your application for <strong>{feedback_request}</strong> has been successful. Click the link below to learn more.",
                'link': f"http://localhost:8000/feedback-request/?request_id={feedback_request.id}",
            }
        )
        email_subject = f'Application for {feedback_request} successful'
        to_list = feedback_request.feedbacker.email
        email = EmailMultiAlternatives(
            email_subject, '-', 'from_email', [to_list])
        email.attach_alternative(html_message, "text/html")
        email.send()

    notification = Notification(user=feedback_request.feedbacker, other_user=feedback_request.feedbackee,
                                feedback_request=feedback_request, type="FeedbackerChosen")
    notification.save()


def feedback_submitted_notification(feedback_request, current_site):
    message = f"Hi, {feedback_request.feedbackee},\nYou have received feedback." \
              f"for your request: '{feedback_request}'.\n\n" \
              f"Login to see the updates:\nhttp://{current_site}/feedback-request/?request_id={feedback_request.id}\n\nThank you for using our service,\n" \
              f"Your AskAnything team."
    mail_subject = 'You received feedback.'
    to_email = feedback_request.feedbackee.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    if feedback_request.feedbackee.userprofile.notifications:
        email.send()

    notification = Notification(user=feedback_request.feedbackee, other_user=feedback_request.feedbacker,
                                feedback_request=feedback_request, type="FeedbackSubmitted")
    notification.save()


def feedbacker_rated_notification(feedback_request, current_site):
    message = f"Hi, {feedback_request.feedbacker},\nYou have been rated for your work on." \
              f": '{feedback_request}'.\n\n" \
              f"Login to see the updates:\nhttp://{current_site}/feedback-request/?request_id={feedback_request.id}\n\nThank you for using our service,\n" \
              f"Your AskAnything team."
    mail_subject = 'You have been rated.'
    to_email = feedback_request.feedbacker.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    if feedback_request.feedbacker.userprofile.notifications:
        email.send()

    notification = Notification(user=feedback_request.feedbacker, other_user=feedback_request.feedbackee,
                                feedback_request=feedback_request, type="FeedbackerRated")
    notification.save()


def new_message_notification(feedback_request, current_site, sender, receiver):
    message = f"Hi, {receiver},\nYou have received a new message on." \
              f": '{feedback_request}'.\n\n" \
              f"Login to see the updates:\nhttp://{current_site}/feedback-request/?request_id={feedback_request.id}\n\nThank you for using our service,\n" \
              f"Your AskAnything team."
    mail_subject = 'New message'
    to_email = receiver.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    if receiver.userprofile.notifications:
        email.send()

    past_messages = Notification.objects.filter(feedback_request=feedback_request, type="NewMessage")
    past_messages.delete()

    notification = Notification(user=receiver, other_user=sender, feedback_request=feedback_request, type="NewMessage")
    notification.save()


def recommended_request_notification(feedback_request, current_site, receiver):
    message = f"Hi, {receiver},\nWe think you may like this feedback request" \
              f": '{feedback_request}'.\n\n" \
              f"\nhttp://{current_site}/feedback-request/?request_id={feedback_request.id}\n\nThank you for using our service,\n" \
              f"Your AskAnything team."
    mail_subject = 'Recommended Feedback Request'
    to_email = receiver.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    if receiver.userprofile.notifications:
        email.send()

    notification = Notification(user=receiver, other_user=feedback_request.feedbackee,
                                feedback_request=feedback_request, type="Recommendation")
    notification.save()
