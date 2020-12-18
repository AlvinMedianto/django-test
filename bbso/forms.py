import re

from crispy_forms.bootstrap import TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Fieldset, LayoutObject, HTML, ButtonHolder, Submit, Row, Column
from crispy_forms.utils import TEMPLATE_PACK
from django.forms import ModelForm, Textarea, inlineformset_factory
from django.template.loader import render_to_string

from bbso.models import BBSORecords, BBSORecordActions


class Formset(LayoutObject):
    template = 'bbso/_formset.html'

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {'formset': formset}, context['request'])


class BBSORecordsForm(ModelForm):
    class Meta:
        model = BBSORecords
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BBSORecordsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('location_details'),
                Field('PTW'),
                Field('JSA'),
                Field('details_of_observation'),
                TabHolder(
                    Tab(
                        'SOS Actions',
                        Fieldset('Add SOS Actions', Formset('bbso_record_actions')),
                    ),
                ),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
            )
        )


class BBSORecordActionsForm(ModelForm):
    class Meta:
        model = BBSORecordActions
        fields = '__all__'
        widgets = {
            'recommended_action': Textarea(attrs={'rows': 2, 'cols': 25}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        formtag_prefix = re.sub('-[0-9]+$', '', kwargs.get('prefix', ''))

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('recommended_action', css_class='form-group col-md-5 mb-0'),
                css_class='formset_row-{}'.format(formtag_prefix)
            ),
        )


BBSORecordActionsFormset = inlineformset_factory(
    BBSORecords,
    BBSORecordActions,
    fields=['recommended_action'],
    form=BBSORecordActionsForm,
    extra=2,
    can_delete=True
)
