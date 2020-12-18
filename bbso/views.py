from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView

from bbso.forms import BBSORecordsForm, BBSORecordActionsFormset
from bbso.models import BBSORecords


class BBSORecordNestedFormCreateView(CreateView):
    model = BBSORecords
    form_class = BBSORecordsForm
    template_name = 'bbso/index.html'

    def get_context_data(self, **kwargs):
        data = super(BBSORecordNestedFormCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['bbso_record_actions'] = BBSORecordActionsFormset(self.request.POST)
        else:
            data['bbso_record_actions'] = BBSORecordActionsFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        bbso_record_actions = context['bbso_record_actions']
        with transaction.atomic():
            form.instance.observer_name_ID = self.request.user
            self.object = form.save()

            if bbso_record_actions.is_valid():
                bbso_record_actions.instance = self.object
                bbso_record_actions.save()
        return super(BBSORecordNestedFormCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bbso_records_detail', kwargs={'pk': self.object.pk})
