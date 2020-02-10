from .models import Notification
from datetime import datetime
from django.utils import timezone
from django.core.mail import EmailMessage


def new_candidate_notification(feedback_request,current_site,candidate):
    mail_subject = 'New candidate for your feedback request'
    to_email = feedback_request.feedbackee.email
    message = f"Hi, {feedback_request.feedbackee},\nYou have a new candidate for your Request: '{feedback_request}'." \
                f"\n\nLogin to see the updates:\nhttp://{current_site}\n\nThank you for using our service,\n" \
                f"Your AskAnything team."
    email = EmailMessage(mail_subject, message, to=[to_email])

    if feedback_request.feedbackee.userprofile.notifications:
        email.send()

    notification = Notification(user=feedback_request.feedbackee, other_user=candidate,feedback_request=feedback_request,type="Candidate")
    notification.save()

def chosen_as_feedbacker_notification(feedback_request,current_site):
    mail_subject = f"AskAnything"
    to_email = feedback_request.feedbacker.email
    message = f"Hi, {feedback_request.feedbacker},\n{feedback_request.feedbackee} has chosen you as a feedbacker" \
                    f"for '{feedback_request}'.\n\n" \
                    f"Login to see the updates:\nhttp://{current_site}\n\nThank you for using our service,\n" \
                    f"Your AskAnything team."
    email = EmailMessage(mail_subject, message, to=[to_email])
    if feedback_request.feedbacker.userprofile.notifications:
        email.send()

    notification = Notification(user=feedback_request.feedbacker, other_user=feedback_request.feedbackee, feedback_request=feedback_request,type="FeedbackerChosen")
    notification.save()

def feedback_submitted_notification(feedback_request,current_site):
    message = f"Hi, {feedback_request.feedbackee},\nYou have received feedback." \
                    f"for your request: '{feedback_request}'.\n\n" \
                    f"Login to see the updates:\nhttp://{current_site}\n\nThank you for using our service,\n" \
                    f"Your AskAnything team."
    mail_subject = 'You received feedback.'
    to_email = feedback_request.feedbackee.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    if feedback_request.feedbackee.userprofile.notifications:
        email.send()

    notification = Notification(user=feedback_request.feedbackee, other_user=feedback_request.feedbacker, feedback_request=feedback_request,type="FeedbackSubmitted")
    notification.save()

def feedbacker_rated_notification(feedback_request,current_site):
    message = f"Hi, {feedback_request.feedbacker},\nYou have been rated for your work on." \
                    f": '{feedback_request}'.\n\n" \
                    f"Login to see the updates:\nhttp://{current_site}\n\nThank you for using our service,\n" \
                    f"Your AskAnything team."
    mail_subject = 'You have been rated.'
    to_email = feedback_request.feedbacker.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    if feedback_request.feedbacker.userprofile.notifications:
        email.send()

    notification = Notification(user=feedback_request.feedbacker,other_user=feedback_request.feedbackee, feedback_request=feedback_request,type="FeedbackerRated")
    notification.save()
