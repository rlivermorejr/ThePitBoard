from django import forms
from appuser.models import UserModel


class EditProfile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfile, self).__init__(*args, **kwargs)
        self.fields['profile_image'].default = self.instance.profile_image

    class Meta:
        model = UserModel
        fields = [
            # 'username',
            'bio',
            'date_of_birth',
            'profile_image'
        ]
