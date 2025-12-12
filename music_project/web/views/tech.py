from django.shortcuts import render, redirect
from web.NetworkHelper import NetworkHelper
from web.performance import benchmark_threading
import plotly.express as px
import plotly.io as pio
import pandas as pd

def external_api_view(request):
    helper = NetworkHelper()
    endpoint = 'songs'
    if request.method == 'POST':
        item_id = request.POST.get('id_to_delete')
        if item_id: helper.delete_item(endpoint, item_id)
        return redirect('external_data')
    external_data = helper.get_list(endpoint)
    return render(request, 'web/external_data.html', {'data': external_data})

def performance_dashboard(request):
    run_test = request.GET.get('run_test')
    chart_html = None
    results = []
    
    if run_test:
        results = benchmark_threading(query_count=100)
        best_result = min(results, key=lambda x: x['time'])
        
        df = pd.DataFrame(results)
        fig = px.line(df, x='workers', y='time', markers=True, 
                      title='Залежність часу виконання від кількості потоків',
                      labels={'workers': 'Кількість потоків', 'time': 'Час виконання (сек)'})
        fig.add_annotation(x=best_result['workers'], y=best_result['time'], text="Оптимум", showarrow=True, arrowhead=1)
        chart_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    return render(request, 'web/performance.html', {'chart': chart_html, 'results': results, 'is_running': run_test})