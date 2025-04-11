from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from ..models.trafego_originado import TrafegoOriginadoIndicador
from ..forms.trafego_originado import TrafegoOriginadoForm

class TrafegoOriginadoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TrafegoOriginadoIndicador
    form_class = TrafegoOriginadoForm
    template_name = 'questionarios/trafego_originado_form.html'
    success_url = reverse_lazy('questionarios:trafego_originado_list')
    permission_required = 'questionarios.add_trafegooriginadoindicador'

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

class TrafegoOriginadoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TrafegoOriginadoIndicador
    template_name = 'questionarios/trafego_originado_list.html'
    context_object_name = 'trafego_originado_list'
    permission_required = 'questionarios.view_trafegooriginadoindicador'

    def get_queryset(self):
        queryset = super().get_queryset()
        operadora = self.request.GET.get('operadora')
        if operadora:
            queryset = queryset.filter(operadora=operadora)
        return queryset.order_by('-ano', '-mes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orange_list'] = self.model.objects.filter(operadora='orange')
        context['mtn_list'] = self.model.objects.filter(operadora='mtn')
        return context

class TrafegoOriginadoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = TrafegoOriginadoIndicador
    form_class = TrafegoOriginadoForm
    template_name = 'questionarios/trafego_originado_form.html'
    success_url = reverse_lazy('questionarios:trafego_originado_list')
    permission_required = 'questionarios.change_trafegooriginadoindicador'

    def form_valid(self, form):
        form.instance.atualizado_por = self.request.user
        return super().form_valid(form)

class TrafegoOriginadoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = TrafegoOriginadoIndicador
    template_name = 'questionarios/trafego_originado_confirm_delete.html'
    success_url = reverse_lazy('questionarios:trafego_originado_list')
    permission_required = 'questionarios.delete_trafegooriginadoindicador'

class TrafegoOriginadoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = TrafegoOriginadoIndicador
    template_name = 'questionarios/trafego_originado_detail.html'
    context_object_name = 'indicador'
    permission_required = 'questionarios.view_trafegooriginadoindicador'

class TrafegoOriginadoResumoView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TrafegoOriginadoIndicador
    template_name = 'questionarios/trafego_originado_resumo.html'
    context_object_name = 'indicadores'
    permission_required = 'questionarios.view_trafegooriginadoindicador'

    def get_queryset(self):
        ano = self.kwargs.get('ano')
        operadora = self.request.GET.get('operadora')
        queryset = self.model.objects.filter(ano=ano)
        if operadora:
            queryset = queryset.filter(operadora=operadora)
        return queryset.order_by('mes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ano = self.kwargs.get('ano')
        operadora = self.request.GET.get('operadora')
        indicadores = self.get_queryset()

        # Cálculos trimestrais
        totais_trimestrais = []
        for trimestre in range(1, 5):
            meses = range((trimestre - 1) * 3 + 1, trimestre * 3 + 1)
            dados_trimestre = indicadores.filter(mes__in=meses)
            
            total_dados_3g = sum(dado.calcular_total_dados_3g() for dado in dados_trimestre)
            total_dados_4g = sum(dado.calcular_total_dados_4g() for dado in dados_trimestre)
            total_sms = sum(dado.calcular_total_sms() for dado in dados_trimestre)
            total_voz = sum(dado.calcular_total_voz() for dado in dados_trimestre)
            total_chamadas = sum(dado.calcular_total_chamadas() for dado in dados_trimestre)
            
            totais_trimestrais.append({
                'trimestre': trimestre,
                'total_dados_3g': total_dados_3g,
                'total_dados_4g': total_dados_4g,
                'total_sms': total_sms,
                'total_voz': total_voz,
                'total_chamadas': total_chamadas
            })

        # Cálculos anuais
        total_dados_3g_anual = sum(dado.calcular_total_dados_3g() for dado in indicadores)
        total_dados_4g_anual = sum(dado.calcular_total_dados_4g() for dado in indicadores)
        total_sms_anual = sum(dado.calcular_total_sms() for dado in indicadores)
        total_voz_anual = sum(dado.calcular_total_voz() for dado in indicadores)
        total_chamadas_anual = sum(dado.calcular_total_chamadas() for dado in indicadores)

        context['ano'] = ano
        context['operadora_selecionada'] = operadora
        context['totais_trimestrais'] = totais_trimestrais
        context['total_dados_3g_anual'] = total_dados_3g_anual
        context['total_dados_4g_anual'] = total_dados_4g_anual
        context['total_sms_anual'] = total_sms_anual
        context['total_voz_anual'] = total_voz_anual
        context['total_chamadas_anual'] = total_chamadas_anual

        return context