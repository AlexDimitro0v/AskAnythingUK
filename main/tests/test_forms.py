from django.test import TestCase
from main.forms import NewFeedbackRequestForm, FeedbackerCommentsForm, FeedbackerRatingForm, ApplicationForm, MessageForm


class Forms(TestCase):
    def test_new_feedback_request(self):
        form_data = {"area" : 1, "title" : "Test", "maintext" : "Test", "reward" : 500, "timelimit" : 20}
        form = NewFeedbackRequestForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {"area" : 1, "title" : "Test", "maintext" : "Test", "reward" : -10, "timelimit" : 20}
        form = NewFeedbackRequestForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {"area" : 1, "title" : "Test", "maintext" : "Test", "reward" : -10, "timelimit" : 0}
        form = NewFeedbackRequestForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_feedback_form(self):
        form_data = {"comments" : "Test"}
        form = FeedbackerCommentsForm(data=form_data)
        self.assertTrue(form.is_valid())

        # No comments required
        form_data = {}
        form = FeedbackerCommentsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_rating_form(self):
        form_data = {"overall" : 5, "quality" : 4, "speed" : 1, "communication" : 2, "review" : "Test"}
        form = FeedbackerRatingForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {"overall" : 5, "quality" : 4, "speed" : 1, "communication" : 2}
        form = FeedbackerRatingForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {"overall" : -1, "quality" : 4, "speed" : 1, "communication" : 2}
        form = FeedbackerRatingForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {"overall" : 6, "quality" : 4, "speed" : 1, "communication" : 2}
        form = FeedbackerRatingForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_application_form(self):
        form_data = {"application" : "Test"}
        form = ApplicationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_message_form(self):
        form_data = {"message" : "Test"}
        form = MessageForm(data=form_data)
        self.assertTrue(form.is_valid())
