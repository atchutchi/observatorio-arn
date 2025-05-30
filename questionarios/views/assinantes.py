from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from ..models import AssinantesIndicador
from ..forms import AssinantesIndicadorForm
from .base_views import FilteredListView

class AssinantesCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = AssinantesIndicador
    form_class = AssinantesIndicadorForm
    template_name = 'questionarios/assinantes_form.html'
    success_url = reverse_lazy('questionarios:assinantes_list')
    permission_required = 'questionarios.add_assinantesindicador'

    # Assinantes model doesn't have criado_por/atualizado_por
    # def form_valid(self, form):
    #     form.instance.criado_por = self.request.user
    #     return super().form_valid(form)

class AssinantesListView(FilteredListView):
    model = AssinantesIndicador
    template_name = 'questionarios/assinantes_list.html'
    context_object_name = 'object_list'
    permission_required = 'questionarios.view_assinantesindicador'

class AssinantesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = AssinantesIndicador
    form_class = AssinantesIndicadorForm
    template_name = 'questionarios/assinantes_form.html'
    success_url = reverse_lazy('questionarios:assinantes_list')
    permission_required = 'questionarios.change_assinantesindicador'

    # def form_valid(self, form):
    #     form.instance.atualizado_por = self.request.user
    #     return super().form_valid(form)

class AssinantesDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = AssinantesIndicador
    template_name = 'questionarios/assinantes_confirm_delete.html'
    success_url = reverse_lazy('questionarios:assinantes_list')
    permission_required = 'questionarios.delete_assinantesindicador'

class AssinantesDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = AssinantesIndicador
    template_name = 'questionarios/assinantes_detail.html'
    context_object_name = 'indicador'
    permission_required = 'questionarios.view_assinantesindicador' 