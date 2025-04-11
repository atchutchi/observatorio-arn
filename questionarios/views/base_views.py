from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

MONTH_CHOICES = [
    (1, "Janeiro"), (2, "Fevereiro"), (3, "Março"), (4, "Abril"), 
    (5, "Maio"), (6, "Junho"), (7, "Julho"), (8, "Agosto"), 
    (9, "Setembro"), (10, "Outubro"), (11, "Novembro"), (12, "Dezembro")
]

class FilteredListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Base ListView with filtering capabilities and month choices."""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        operadora = self.request.GET.get('operadora')
        ano = self.request.GET.get('ano')
        mes = self.request.GET.get('mes')

        if operadora:
            queryset = queryset.filter(operadora=operadora)
        if ano:
            try:
                queryset = queryset.filter(ano=int(ano))
            except ValueError:
                pass # Ignore invalid year input
        if mes:
            try:
                queryset = queryset.filter(mes=int(mes))
            except ValueError:
                pass # Ignore invalid month input
                
        return queryset.order_by('-ano', '-mes') # Default ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mes_choices'] = MONTH_CHOICES
        return context 