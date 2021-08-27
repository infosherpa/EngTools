from django import forms
from .models import TunnelFrame, LoadDefinition
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Row, Column, Button, Hidden, HTML, BaseInput
from crispy_forms.bootstrap import FormActions, AppendedText, PrependedAppendedText, PrependedText, InlineCheckboxes


class TunnelInputForm(forms.ModelForm):

    class Meta:
        model = TunnelFrame
        fields = ['frame_description', 'dimension_system', 'plane', 'frame_inner_height', 'frame_outer_height',
                  'frame_inner_width', 'frame_outer_width',
                  'haunch_depth', 'haunch_width', 'roof_slab_thickness', 'concourse_slab_thickness',
                  'concourse_haunch_depth', 'concourse_haunch_width', 'column_bays',
                  'column_capital_height', 'column_capital_width', 'concourse_slab_vertical_location', 'column_width']

    def clean(self):
        """Sanity check of measurements"""
        super().clean()
        inner_h, outer_h = self.cleaned_data['frame_inner_height'], self.cleaned_data['frame_outer_height']
        inner_l, outer_l = self.cleaned_data['frame_inner_width'], self.cleaned_data['frame_outer_width']
        haunch_d, haunch_w = self.cleaned_data['haunch_depth'], self.cleaned_data['haunch_width']
        concourse_slab_thickness = self.cleaned_data['concourse_slab_thickness']
        concourse_slab_vertical_location = self.cleaned_data['concourse_slab_vertical_location']
        concourse_haunch_depth, concourse_haunch_width = self.cleaned_data['concourse_haunch_width'], self.cleaned_data['concourse_haunch_depth']
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
        if concourse_slab_thickness:
            if not concourse_haunch_depth or concourse_haunch_width:
                raise ValidationError(_('Input 0 if no Haunch on Concourse level'), code='invalid')


class TunnelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_show_labels = True
        self.helper.form_class = 'form-horizontal'
        self.fields['concourse_slab_vertical_location'].label = "Concourse Slab Z-axis Centroid"
        self.fields['column_capital_height'].label = "Column Capital Height - CS"
        self.fields['column_capital_width'].label = "Column Capital Width - CS"
        self.fields['column_capital_roof_slab_height'].label = "Column Capital Height - RS"
        self.fields['column_capital_roof_slab_width'].label = "Column Capital Width - RS"
        self.fields['column_bays'].label = "Column Divided Bays"
        self.fields['concrete_strength_walls'].label = "Concrete Strength Walls (PSI)"
        self.fields['concrete_strength_slabs'].label = "Concrete Strength Slabs (PSI)"
        self.fields['concrete_strength_columns'].label = "Concrete Strength Columns (PSI)"
        self.fields['base_restraint'].label = "Frame Restrained at Base"

        self.fields['column_capital_roof_slab_height'].widget.attrs['readonly'] = True
        self.fields['column_capital_roof_slab_width'].widget.attrs['readonly'] = True
        self.fields['column_capital_height'].widget.attrs['readonly'] = True
        self.fields['column_capital_width'].widget.attrs['readonly'] = True
        self.fields['column_width'].widget.attrs['readonly'] = True

        self.fields['concourse_haunch_depth'].widget.attrs['readonly'] = True
        self.fields['concourse_haunch_width'].widget.attrs['readonly'] = True
        self.fields['concourse_slab_vertical_location'].widget.attrs['readonly'] = True


        self.helper.layout = Layout(
                Div(
                Div(
                Row(
                    Column(
                        Div(
                        HTML("<p class='pt-3 px-2'>1.  Input Frame Dimensions (* for required fields)</p>"),
                        HTML("<p class='px-2'>2.  Generate Frame</p>"),
                        HTML("<p class='px-2'>3.  Download a SAP-2000 Compatible Excel file</p>"),
                        css_class="border-bottom border-top border-dark border-3"),
                        css_class="col-md-10 mb-2"),
                ),
                Row(
                    Column(
                        Field('frame_description', css_class='form-control'),
                        css_class='form-group col-md-5 mb-0'),
                    Column(
                        Field('dimension_system', css_class='form-select'),
                        css_class='form-group col-md-5 mb-0')
                    ),
                Row(
                    Column(
                        Field('plane', css_class='form-select'),
                        css_class='form-group col-md-5 mb-0'),
                    Column(
                        Field('inverse_slab_thickness', css_class='no-spin form-control', min=0),
                        css_class="col-md-5 mb-0"),
                ),
                Row(
                    Column(
                        Field('frame_inner_height', css_class='no-spin form-control', min=0),
                        css_class='form-group col-md-5 mb-0'),
                    Column(
                        Field('frame_outer_height', css_class='no-spin form-control', min=0),
                        css_class='form-group col-md-5 mb-0'),
                    css_class="row form-row"),
                Row(
                    Column(
                        Field('frame_inner_width', css_class='no-spin form-control', min=0),
                        css_class='form-group col-md-5 mb-0'),
                    Column(
                        Field('frame_outer_width', css_class='no-spin form-control', min=0),
                        css_class='form-group col-md-5 mb-0'),
                    css_class="form-row mb-0"),
                Row(
                    Column(
                        Field('haunch_depth', css_class='no-spin form-control', min=0),
                        css_class='form-group col-md-5 mb-0'),
                    Column(
                        Field('haunch_width', css_class='no-spin form-control', min=0),
                        css_class='form-group col-md-5 mb-0'),
                    css_class="form-row mb-0"),
                Row(
                    Column(
                        Field('concrete_strength_walls', css_class='no-spin form-control', min=0),
                        css_class='form-group col-md-5 mb-0'),
                    Column(
                        Div(
                            Field('concrete_strength_slabs', css_class='no-spin form-control', aria_describedby="basic-addon3", min=0),
                            css_class="form-group"),
                        css_class='col-md-5 mb-0'),
                    css_class="form-group row mb-0"),
                Row(
                    Column(
                        Field('slab_stiffness_modifier', css_class='no-spin form-control', min=0),
                        css_class='col-md-5 mb-0'),
                    Column(
                        Field('wall_stiffness_modifier', css_class='no-spin form-control', min=0),
                        css_class='col-md-5 mb-0'),
                    css_class="row"),
                Row(
                    Column(
                        Field('base_restraint'),
                        css_class='col-md-5 my-1'),
                    css_class="row"),
                    id='basic_frame'),

                Div(
                Row(
                        Div(
                        HTML("<p class='mt-2 px-2'>-> Enter Concourse Slab Thickness to create a Concourse Slab for the Frame and enable the Concourse control Elements</p>"),
                        HTML("<p class='px-2'>-> Increase Bays above 1 to Add Columns to the Frame and enable the Column control Elements</p>"),
                        css_class="ml-3 pl-3 border-bottom border-top border-dark border-3"),
                        css_class="col-md-10 mb-3"),
                Row(
                    Column(
                        Field('concourse_slab_thickness', css_class='no-spin form-control', min=0, oninput="concourseControl()"),
                        css_class='form-group col-md-5 mb-0'),
                    Column(
                        Field('concourse_slab_vertical_location', css_class='no-spin form-control', min=0),
                        css_class='form-group col-md-5 mb-0', css_id="chvl"),
                    css_class="form-row mb-0"),
                Row(
                    Column(
                        Field('concourse_haunch_depth', css_class='no-spin form-control', min=0),
                        css_class='form-group col-md-5 mb-0', css_id="chdi"),
                    Column(
                        Field('concourse_haunch_width', css_class='no-spin form-control', min=0),
                        css_class='form-group col-md-5 mb-0', css_id="chwi"),
                    css_class="form-row mb-0"),
                Row(
                    Column(
                        Field('column_bays', css_class='no-spin form-control', min=1, oninput="columnControl()"),
                        css_class='form-group col-md-5 mb-0'),
                    Column(
                        Field('column_width', css_class='no-spin form-control', min=0),
                        css_class='form-group col-md-5 mb-0', css_id="cwi"),
                    css_class="form-row mb-0"),
                Row(
                    Column(
                        Field('column_capital_height', css_class='no-spin form-control', min=0),
                           css_class='form-group col-md-5 mb-0', css_id="cchcs"),
                    Column(
                        Field('column_capital_width', css_class='no-spin form-control', min=0),
                              css_class='form-group form-outline col-md-5 mb-0', css_id="ccwcs"),
                    css_class='form-row mb-0'),
                Row(
                    Column(
                        Field('column_capital_roof_slab_height', css_class='no-spin form-control', min=0),
                        css_class='form-group form-outline col-md-5 mb-0', css_id="ccrsh"),
                    Column(
                        Field('column_capital_roof_slab_width', css_class='no-spin form-control', min=0),
                        css_class='form-group form-outline col-md-5 mb-0', css_id="ccrsw"),
                    css_class="form-row mb-0"),
                Row(
                    Column(
                        Field('column_stiffness_modifier', css_class='no-spin form-control', min=0),
                        css_class='col-md-5 mb-0'),
                    Column(
                        Field('concrete_strength_columns', css_class='no-spin form-control', min=0),
                        css_class='col-md-5 mb-0'),
                    css_class="row"),
                    css_id='conc_col', css_class="mt-3 pt-3", style="display: none;"),


            FormActions(
                Button('_conc', 'Add Concourse/Columns', css_class='btn btn-outline-success', onclick='formAdv()',
                       css_id="formcontrolbut"),
                Submit('_generate', 'Generate', css_class='btn btn-success my-3'),
                Submit('_excel', 'Excel', css_class='btn btn-success my-3'),
                # Submit('_save', 'Save', css_class='btn btn-success my-3')
            css_class="col-md-10 mt-3 border-dark border-bottom border-top border-3"),
        css_class="mb-5"),
        )


    class Meta:

        model = TunnelFrame
        fields = ['frame_description', 'dimension_system', 'plane', 'frame_inner_height', 'frame_outer_height',
                  'frame_inner_width', 'frame_outer_width',
                  'haunch_depth', 'haunch_width', 'inverse_slab_thickness', 'concourse_slab_thickness',
                  'concourse_haunch_depth', 'concourse_haunch_width', 'column_bays',
                  'column_capital_height', 'column_capital_width', 'concourse_slab_vertical_location', 'column_width',
                  'column_capital_roof_slab_height', 'column_capital_roof_slab_width', 'column_stiffness_modifier',
                  'wall_stiffness_modifier', 'slab_stiffness_modifier', 'concrete_strength_walls', 'concrete_strength_slabs',
                  'concrete_strength_columns', 'base_restraint']

    def clean(self):
        """Sanity check of measurements"""
        super().clean()
        inner_h, outer_h = self.cleaned_data['frame_inner_height'], self.cleaned_data['frame_outer_height']
        inner_l, outer_l = self.cleaned_data['frame_inner_width'], self.cleaned_data['frame_outer_width']
        haunch_d, haunch_w = self.cleaned_data['haunch_depth'], self.cleaned_data['haunch_width']
        col_cap_w, col_cap_height = self.cleaned_data['column_capital_width'], self.cleaned_data['column_capital_height']
        col_cap_rsw, col_cap_rsh = self.cleaned_data['column_capital_roof_slab_width'], self.cleaned_data[
            'column_capital_roof_slab_height']
        concourse_slab_thickness = self.cleaned_data['concourse_slab_thickness']
        column_bays = self.cleaned_data['column_bays']
        column_width = self.cleaned_data['column_width']
        concourse_slab_vertical_location = self.cleaned_data['concourse_slab_vertical_location']
        concourse_haunch_depth, concourse_haunch_width = self.cleaned_data['concourse_haunch_width'], self.cleaned_data['concourse_haunch_depth']
        if inner_h and outer_h and inner_l and outer_l:
            if inner_h <= 0 or outer_h <= 0 or inner_l <= 0 or outer_l <= 0:
                raise ValidationError(_('Invalid value'), code='invalid')
            if self.cleaned_data['frame_inner_height'] > self.cleaned_data['frame_outer_height']:
                raise ValidationError(_('Invalid value'), code='invalid')
            if self.cleaned_data['frame_inner_width'] > self.cleaned_data['frame_outer_width']:
                raise ValidationError(_('Invalid value'), code='invalid')
        if column_bays <1:
            raise ValidationError(_('Invalid Bays value'), code='invalid')
        if haunch_d and haunch_w:
            if haunch_d <= 0 or haunch_w <= 0:
                raise ValidationError(_('Invalid value'), code='invalid')
        if concourse_slab_thickness:
            if concourse_haunch_depth is None or concourse_haunch_width is None:
                raise ValidationError(_('Input 0 if no Haunch on Concourse level'), code='invalid')
        if column_bays >1:
            print(column_bays)
            if column_width is None:
                raise ValidationError(_('Invalid value add column width'), code='invalid')
            if column_width <= 0:
                raise ValidationError(_('Invalid value add column width'), code='invalid')
        if col_cap_w or col_cap_height:
            if col_cap_w<=0:
                raise ValidationError(_('Invalid value: Provide Column Capital Width'), code='invalid')
            if col_cap_height<=0:
                raise ValidationError(_('Invalid value: Provide Column Capital Height'), code='invalid')
            if not concourse_slab_thickness or not concourse_slab_vertical_location:
                raise ValidationError(_('Invalid value: Column Capital - CS but no Concourse Slab'), code='invalid')
        if col_cap_rsw or col_cap_rsh:
            if not column_width or column_bays<2:
                raise ValidationError(_('Invalid value - add column data'), code='invalid')
        if column_width:
            if column_bays <= 1:
                raise ValidationError(_('Invalid value: Column Width Defined but no columns - Add Column Divided Bay'), code='invalid')


class LoadDefinitionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.fields['force_start_depth'].label = "Force Starting Depth (mm from Top of Frame)"
        self.fields['force_end_depth'].label = "Force End Depth (mm from Top of Frame)"
        self.fields['start_force'].label = "Initial Force N/mm"
        self.fields['end_force'].label = "End Force N/mm"
        self.helper.layout = Layout(
            Fieldset('Add load to Frame:',
                Row(
                    Column(
                        Field('load_pattern_description', css_class='form-control no-spin', onchange='dirFunc()'),
                        css_class='col-10'),
                ),
                Row(
                    Column(
                        Field('load_direction', css_class='form-control no-spin'),
                        css_class='col-10'),
                ),
                Row(
                    Column(
                        Field('load_location', css_class='form-control no-spin'),
                        css_class='col-10'),
                ),
                Row(
                    Column(
                        Field('start_force', css_class='form-control no-spin'),
                        css_class='col-5'),
                    Column(
                        Field('end_force', css_class='form-control no-spin'),
                        css_class="col-5"),
                ),
                Row(
                    Div(
                        Field('force_start_depth', css_class='form-control no-spin'),
                        css_class='col-5'),
                    Div(
                        Field('force_end_depth', css_class='form-control no-spin'),
                        css_class='col-5'),
                    css_class="row", id="force_depth"),
                     ),
            FormActions(
                Submit('_load', 'Add Load', css_class='btn btn-success my-3')
            ),
        )

    class Meta:

        model = LoadDefinition
        fields = ['load_pattern_description', 'load_direction', 'start_force', 'end_force',
                  'load_location', 'force_start_depth', 'force_end_depth']

    def clean(self):
        load_pattern_description, load_direction = self.cleaned_data['load_pattern_description'], self.cleaned_data['load_direction']
        start_force, end_force = self.cleaned_data['start_force'], self.cleaned_data['end_force']
        force_start_depth, force_end_depth = self.cleaned_data['force_start_depth'], self.cleaned_data['force_end_depth']
        load_location = self.cleaned_data['load_location']


class PartialModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False


class TunnelFormGeometry(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_show_labels = True
        self.helper.form_class = 'form-horizontal geoform'
        self.helper.form_id = 'geo_form'
        self.helper.layout = Layout(
                Hidden('form', 'geo_form'),
                Row(
                    Column(
                        Field('frame_description', css_class='form-control'),
                        css_class='form-group col-md-5 mb-0'),
                ),
                Row(
                    Column(
                        Field('dimension_system', css_class='form-select'),
                        css_class='form-group col-md-5 mb-0'),
                ),
                Row(
                    Column(
                        Field('plane', css_class='form-select'),
                        css_class='form-group col-md-5 mb-0'),
                ),
                Row(
                    Column(
                        Field('frame_inner_height', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    Column(
                        Field('frame_outer_height', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row form-row"),
                Row(
                    Column(
                        Field('frame_inner_width', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    Column(
                        Field('frame_outer_width', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Row(
                    Column(
                        Field('haunch_depth', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    Column(
                        Field('haunch_width', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Row(
                    Column(
                        Field('roof_slab_thickness', css_class='form-control no-spin'),
                        css_class="col-10"),
                    css_class="row"),
                FormActions(
                    Submit('_advance', 'Advance', css_class='btn btn-success my-3')
                )
        )

    class Meta:

        model = TunnelFrame
        fields = ['frame_description', 'dimension_system', 'plane', 'frame_inner_height', 'frame_outer_height',
                  'frame_inner_width', 'frame_outer_width', 'haunch_depth', 'haunch_width', 'roof_slab_thickness']

    def clean(self):
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


class TunnelFormConcourseColumns(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_show_labels = True
        self.helper.form_class = 'form-horizontal tunform'
        self.helper.form_id = "Column Concourse Form"
        self.helper.layout = Layout(
                Row(
                    Column(
                        Field('concourse_slab_thickness', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    Column(
                        Field('concourse_slab_vertical_location', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Row(
                    Column(
                        Field('concourse_haunch_depth', step=1, css_class='form-control no-spin'),
                        css_class='col-auto'),
                    Column(
                        Field('concourse_haunch_width', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Row(
                    Column(
                        Field('column_bays', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    Column(
                        Field('column_width', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Row(
                    Column(
                        Field('column_capital_height', css_class='no-spin form-control'),
                           css_class='col-auto'),
                    Column(
                        Field('column_capital_width', css_class='no-spin form-control'),
                              css_class='col-auto'),
                    css_class='row'),
                Div(
                    Div(
                        Field('column_capital_roof_slab_height', css_class='no-spin form-control'),
                        css_class='col-auto'),
                    Div(
                        Field('column_capital_roof_slab_width', css_class='no-spin form-control'),
                        css_class='col-auto'),
                    css_class="row"),
                Hidden('form', 'concourse_col_form'),
                Field('hash', type="hidden"),
            FormActions(
                Submit('_generate', 'Dimensions', css_class='btn btn-success my-3'),
                Submit('_excel', 'Advance', css_class='btn btn-success formadvance my-3'),
            )
        )

    class Meta:

        model = TunnelFrame
        fields = ['concourse_slab_thickness','concourse_haunch_depth', 'concourse_haunch_width', 'column_bays',
                  'column_capital_height', 'column_capital_width', 'concourse_slab_vertical_location', 'column_width',
                  'column_capital_roof_slab_height', 'column_capital_roof_slab_width', 'hash']

    def clean(self):
        col_cap_w, col_cap_height = self.cleaned_data['column_capital_width'], self.cleaned_data[
            'column_capital_height']
        concourse_slab_thickness = self.cleaned_data['concourse_slab_thickness']
        column_bays = self.cleaned_data['column_bays']
        column_width = self.cleaned_data['column_width']
        concourse_slab_vertical_location = self.cleaned_data['concourse_slab_vertical_location']
        concourse_haunch_depth, concourse_haunch_width = self.cleaned_data['concourse_haunch_width'], self.cleaned_data[
            'concourse_haunch_depth']
        if concourse_slab_thickness:
            if not concourse_haunch_depth or not concourse_haunch_width:
                raise ValidationError(_('Input 0 if no Haunch on Concourse level'), code='invalid')
        if column_bays >1:
            print(column_bays)
            if not column_width:
                raise ValidationError(_('Invalid value add column width'), code='invalid')
            if column_width is None:
                raise ValidationError(_('Invalid value add column width'), code='invalid')
        if col_cap_w or col_cap_height:
            if not concourse_slab_thickness or not concourse_slab_vertical_location:
                raise ValidationError(_('Invalid value Column Capital - CS but no Concourse Slab'))


class TunnelFrameModifiers(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_show_labels = True
        self.helper.form_class = 'form-horizontal tunform'
        self.helper.layout = Layout(
                Row(
                    Column(
                        Field('concrete_strength_walls', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Row(
                    Column(
                        Field('concrete_strength_slabs', step=1, css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Row(
                    Column(
                        Field('concrete_strength_columns', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Row(
                    Column(
                        Field('wall_stiffness_modifier', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Row(
                    Column(
                        Field('slab_stiffness_modifier', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Row(
                    Column(
                        Field('column_stiffness_modifier', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Row(
                    Column(
                        Field('column_depth_for_analysis', css_class='form-control no-spin'),
                        css_class='col-auto'),
                    css_class="row"),
                Hidden('form', 'conc_mod_form'),
                Field('hash', type="hidden"),
                FormActions(
                    Submit('_generate', 'Generate', css_class='button white formfinal my-3'),
                    Submit('_excel', 'Excel', css_class='button white my-3'),
                )
            )

    class Meta:

        model = TunnelFrame
        fields = ['column_stiffness_modifier', 'concrete_strength_slabs', 'concrete_strength_columns',
                  'wall_stiffness_modifier', 'slab_stiffness_modifier', 'concrete_strength_walls', 'hash', 'column_depth_for_analysis']
