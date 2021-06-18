from django import forms
from .models import TunnelFrame
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper


class TunnelInputForm(forms.ModelForm):

    class Meta:
        model = TunnelFrame
        fields = ['frame_description', 'frame_inner_height', 'frame_outer_height',
                  'frame_inner_width', 'frame_outer_width',
                  'haunch_depth', 'haunch_width', 'roof_slab_thickness']

    def clean(self):
        """Sanity check of measurements"""
        super().clean()
        inner_h, outer_h = self.cleaned_data['frame_inner_height'], self.cleaned_data['frame_outer_height']
        inner_l, outer_l = self.cleaned_data['frame_inner_width'], self.cleaned_data['frame_outer_width']
        haunch_d, haunch_w = self.cleaned_data['haunch_depth'], self.cleaned_data['haunch_width']
        if inner_h and outer_h and inner_l and outer_l:
            if inner_h <= 0 or outer_h <= 0 or inner_l <= 0 or outer_l <= 0:
                raise ValidationError(_('Invalid value'), code='invalid')
            if self.cleaned_data['frame_inner_height'] > self.cleaned_data['frame_outer_height']:
                raise ValidationError(_('Invalid value'), code='invalid')
            if self.cleaned_data['frame_inner_width'] > self.cleaned_data['frame_outer_width']:
                raise ValidationError(_('Invalid value'), code='invalid')
        if haunch_d and haunch_w:
            if haunch_d <= 0 or haunch_w <= 0:
                raise ValidationError(_('Invalid value'), code='invalid')

