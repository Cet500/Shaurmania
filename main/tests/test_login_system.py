from django.test import TestCase
from main.models import User
from main.forms import SignUpForm, LoginForm


class SignUpFormTest(TestCase):
	def test_valid_form_creates_user(self):
		form_data = {
			"username":  "sergey",
			"email":     "sergey@example.com",
			"password1": "StrongPass123",
			"password2": "StrongPass123",
		}
		form = SignUpForm(data=form_data)
		self.assertTrue(form.is_valid())
		user = form.save()
		self.assertEqual(user.username, "sergey")
		self.assertTrue(User.objects.filter(username="sergey").exists())

	def test_passwords_must_match(self):
		form_data = {
			"username": "sergey",
			"email": "sergey@example.com",
			"password1": "12345",
			"password2": "54321",
		}
		form = SignUpForm(data=form_data)
		self.assertFalse(form.is_valid())
		self.assertIn("Пароли не совпадают", form.errors["__all__"])

	def test_email_is_required(self):
		form_data = {
			"username": "sergey",
			"password1": "StrongPass123",
			"password2": "StrongPass123",
		}
		form = SignUpForm(data=form_data)
		self.assertFalse(form.is_valid())
		self.assertIn("email", form.errors)

	def test_widgets_have_correct_class(self):
		form = SignUpForm()
		for field in ["username", "email", "password1", "password2"]:
			self.assertIn("form__input", form.fields[field].widget.attrs.get("class", ""))


class LoginFormTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user( email = "sergey@example.com", username="sergey", password="StrongPass123")

	def test_valid_login(self):
		form = LoginForm(data={"username": "sergey", "password": "StrongPass123"})
		self.assertTrue(form.is_valid())

	def test_invalid_login_wrong_password(self):
		form = LoginForm(data={"username": "sergey", "password": "wrong"})
		self.assertFalse(form.is_valid())

	def test_widgets_have_correct_class(self):
		form = LoginForm()
		for field in ["username", "password"]:
			self.assertIn("form__input", form.fields[field].widget.attrs.get("class", ""))
