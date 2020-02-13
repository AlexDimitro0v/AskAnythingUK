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
                'link': f"http://{current_site}/feedback-request/?request_id={feedback_request.id}",
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
                'link': f"http://{current_site}/feedback-request/?request_id={feedback_request.id}",
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
    if feedback_request.feedbackee.userprofile.notifications:
        html_message = render_to_string(
            'main/email-template.html',
            {
                'title': feedback_request,
                'user': feedback_request.feedbackee,
                'message': f"Your have received feedback for <strong>{feedback_request}</strong>. Click the link below to learn more.",
                'link': f"http://{current_site}/feedback-request/?request_id={feedback_request.id}",
            }
        )
        email_subject = f'Feedback for {feedback_request} received'
        to_list = feedback_request.feedbackee.email
        email = EmailMultiAlternatives(
            email_subject, '-', 'from_email', [to_list])
        email.attach_alternative(html_message, "text/html")
        email.send()

    notification = Notification(user=feedback_request.feedbackee, other_user=feedback_request.feedbacker,
                                feedback_request=feedback_request, type="FeedbackSubmitted")
    notification.save()


def feedbacker_rated_notification(feedback_request, current_site):
    if feedback_request.feedbacker.userprofile.notifications:
        html_message = render_to_string(
            'main/email-template.html',
            {
                'title': feedback_request,
                'user': feedback_request.feedbacker,
                'message': f"Your have been rated for your work on <strong>{feedback_request}</strong>. Click the link below to learn more.",
                'link': f"http://{current_site}/feedback-request/?request_id={feedback_request.id}",
            }
        )
        email_subject = f'Rating for {feedback_request} received'
        to_list = feedback_request.feedbacker.email
        email = EmailMultiAlternatives(
            email_subject, '-', 'from_email', [to_list])
        email.attach_alternative(html_message, "text/html")
        email.send()

    notification = Notification(user=feedback_request.feedbacker, other_user=feedback_request.feedbackee,
                                feedback_request=feedback_request, type="FeedbackerRated")
    notification.save()


def new_message_notification(feedback_request, current_site, sender, receiver):
    if receiver.userprofile.notifications:
        html_message = render_to_string(
            'main/email-template.html',
            {
                'title': feedback_request,
                'user': receiver,
                'message': f"You have received a new message on <strong>{feedback_request}</strong>. Click the link below to learn more.",
                'link': f"http://{current_site}/feedback-request/?request_id={feedback_request.id}",
            }
        )
        email_subject = f'New Message'
        to_list = receiver.email
        email = EmailMultiAlternatives(
            email_subject, '-', 'from_email', [to_list])
        email.attach_alternative(html_message, "text/html")
        email.send()

    # Delete all previous notification message instances
    past_messages = Notification.objects.filter(feedback_request=feedback_request, type="NewMessage")
    past_messages.delete()

    notification = Notification(user=receiver, other_user=sender, feedback_request=feedback_request, type="NewMessage")
    notification.save()


def recommended_request_notification(feedback_request, current_site, receiver):
    if receiver.userprofile.notifications:
        html_message = render_to_string(
            'main/email-template.html',
            {
                'title': feedback_request,
                'user': receiver,
                'message': f"We think you may like this feedback request <strong>{feedback_request}</strong>. Click the link below to learn more.",
                'link': f"http://{current_site}/feedback-request/?request_id={feedback_request.id}",
            }
        )
        email_subject = 'Recommended Feedback Request'
        to_list = receiver.email
        email = EmailMultiAlternatives(
            email_subject, '-', 'from_email', [to_list])
        email.attach_alternative(html_message, "text/html")
        email.send()

    notification = Notification(user=receiver, other_user=feedback_request.feedbackee,
                                feedback_request=feedback_request, type="Recommendation")
    notification.save()


def money_released_notification(feedback_request, current_site):
    if feedback_request.feedbacker.userprofile.notifications:
        html_message = render_to_string(
            'main/email-template.html',
            {
                'title': feedback_request,
                'user': feedback_request.feedbacker,
                'message': f"Your reaward for <strong>{feedback_request}</strong> has been released by the feedbackee. Click the link below to learn more.",
                'link': f"http://{current_site}/feedback-request/?request_id={feedback_request.id}",
            }
        )
        email_subject = f'Money for {feedback_request} released'
        to_list = feedback_request.feedbacker.email
        email = EmailMultiAlternatives(
            email_subject, '-', 'from_email', [to_list])
        email.attach_alternative(html_message, "text/html")
        email.send()

    notification = Notification(user=feedback_request.feedbacker, other_user=feedback_request.feedbackee,
                                feedback_request=feedback_request, type="MoneyRelease")
    notification.save()
