from django.contrib.auth.forms import AuthenticationForm


class LogoutForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label.title()
            field.widget.attrs['class'] = "login_text_widget"

