from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from realtyapp.daos import RealtyDAO
from realtyapp.forms import RealtyForm, SearchForm
from realtyapp.use_cases import CreateRealtyUseCase, ListRealtyByAddressUseCase


class AddRealtyView(FormView):
    form_class = RealtyForm
    success_url = reverse_lazy('realtyapp:index')
    template_name = 'add_realty.html'

    def form_valid(self, form):
        use_case = CreateRealtyUseCase(RealtyDAO())
        use_case.execute(**form.cleaned_data)
        return super(AddRealtyView, self).form_valid(form)


class IndexView(ListView):
    paginate_by = 20
    template_name = 'index.html'
    form_class = SearchForm

    @property
    def queryset(self):
        use_case = ListRealtyByAddressUseCase(RealtyDAO())
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return list(use_case.execute(**form.cleaned_data))
        return list(use_case.execute())

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        form = self.form_class(self.request.GET)

        if not form.is_valid():
            form = self.form_class()
        context.update({'form': form})

        return context
