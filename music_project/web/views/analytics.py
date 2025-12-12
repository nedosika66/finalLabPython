from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from web.services import get_aggregated_data, get_song_statistics
from music_app.models import Song, Artist
import plotly.express as px
import plotly.io as pio
import csv
from math import pi
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.transform import cumsum
from bokeh.resources import CDN

def dashboard_api(request):
    data = get_aggregated_data()
    stats = get_song_statistics()
    response_data = {'statistics': stats}
    for key, df in data.items():
        response_data[key] = df.to_dict('records')
    return JsonResponse(response_data)

def _get_filter_params(request):
    filter_type = request.GET.get('filter_type', 'year')
    min_year, max_year = 1950, 2025
    selected_genre = request.GET.get('genre')
    selected_country = request.GET.get('country')

    if filter_type == 'year':
        try: 
            min_year = int(request.GET.get('min_year', 1950))
        except (ValueError, TypeError): 
            pass
        try: 
            max_year = int(request.GET.get('max_year', 2025))
        except (ValueError, TypeError): 
            pass
    
    return filter_type, min_year, max_year, selected_genre, selected_country

def dashboard(request):
    filter_type, min_year, max_year, selected_genre, selected_country = _get_filter_params(request)

    data = get_aggregated_data(
        min_year=min_year if filter_type == 'year' else None,
        max_year=max_year if filter_type == 'year' else None,
        genre_filter=selected_genre,
        country_filter=selected_country
    )

    stats = get_song_statistics()

    def create_chart_html(fig):
        fig.update_layout(
            autosize=True,
            margin=dict(t=80, b=120, l=40, r=40),
            legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
            title=dict(y=0.95, x=0.5, xanchor='center', yanchor='top', font=dict(size=20))
        )
        return pio.to_html(fig, full_html=False, include_plotlyjs='cdn', config={'responsive': True})

    charts = {}

    if not data['genres_df'].empty:
        fig = px.pie(data['genres_df'], names='genre__name', values='total_songs', title='Топ-10 Жанрів')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        charts['chart1'] = create_chart_html(fig)
    else: charts['chart1'] = "Дані відсутні"

    if not data['years_df'].empty:
        fig = px.line(data['years_df'], x='release_year', y='avg_duration', title='Середня тривалість (хв)', markers=True)
        fig.update_yaxes(title_text="Хвилини", tickformat=".2f")
        charts['chart2'] = create_chart_html(fig)
    else: charts['chart2'] = "Дані відсутні"

    if not data['artists_df'].empty:
        fig = px.bar(data['artists_df'], x='nickname', y='filtered_song_count', title='Топ Артистів', color='filtered_song_count')
        charts['chart3'] = create_chart_html(fig)
    else: charts['chart3'] = "Дані відсутні"

    if not data['albums_df'].empty:
        fig = px.bar(data['albums_df'], x='title', y='filtered_track_count', title='Топ Альбомів')
        charts['chart4'] = create_chart_html(fig)
    else: charts['chart4'] = "Дані відсутні"

    if not data['countries_df'].empty:
        fig = px.pie(data['countries_df'], names='country', values='artist_count', title='Топ Країн')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        charts['chart5'] = create_chart_html(fig)
    else: charts['chart5'] = "Дані відсутні"

    if not data['producers_df'].empty:
        fig = px.bar(data['producers_df'], x='nickname', y='filtered_prod_count', title='Топ Продюсерів')
        charts['chart6'] = create_chart_html(fig)
    else: charts['chart6'] = "Дані відсутні"

    context = {
        **charts,
        'stats': stats,
        'filter_type': filter_type, 'min_year': min_year, 'max_year': max_year,
        'all_genres': Song.objects.values_list('genre__name', flat=True).distinct().order_by('genre__name'),
        'all_countries': Artist.objects.exclude(country='').exclude(country__isnull=True).values_list('country', flat=True).distinct().order_by('country'),
        'selected_genre': selected_genre, 'selected_country': selected_country
    }
    return render(request, 'web/dashboard.html', context)

def dashboard_bokeh(request):
    filter_type, min_year, max_year, selected_genre, selected_country = _get_filter_params(request)
    debug_log = []

    try:
        data = get_aggregated_data(
            min_year=min_year if filter_type == 'year' else None,
            max_year=max_year if filter_type == 'year' else None,
            genre_filter=selected_genre,
            country_filter=selected_country
        )
    except Exception as e:
        debug_log.append(f"Error fetching data: {e}")
        data = {}

    stats = get_song_statistics()
    plots = {}
    COLORS = ['#0d6efd', '#198754', '#dc3545', '#ffc107', '#0dcaf0', '#6610f2', '#fd7e14', '#20c997', '#e83e8c', '#6c757d'] * 5

    if data and not data['genres_df'].empty:
        try:
            df = data['genres_df'].copy()
            df['angle'] = df['total_songs'] / df['total_songs'].sum() * 2 * pi
            df['color'] = COLORS[:len(df)]
            p = figure(height=400, title="Топ-10 Жанрів", toolbar_location=None, tools="hover", tooltips="@genre__name: @total_songs", x_range=(-0.5, 1.0))
            p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color', legend_field='genre__name', source=ColumnDataSource(df))
            p.axis.visible = False; p.grid.grid_line_color = None
            plots['chart1'] = p
        except Exception as e: debug_log.append(str(e))

    if data and not data['years_df'].empty:
        try:
            source = ColumnDataSource(data['years_df'])
            p = figure(title="Середня тривалість (хв)", height=400, x_axis_label='Рік', y_axis_label='Хв', tools="hover", tooltips=[("Рік", "@release_year"), ("Час", "@avg_duration")])
            p.line(x='release_year', y='avg_duration', source=source, line_width=3, color="#0d6efd")
            p.scatter(x='release_year', y='avg_duration', source=source, size=8, color="#0d6efd")
            plots['chart2'] = p
        except Exception as e: debug_log.append(str(e))

    if data and not data['artists_df'].empty:
        try:
            df = data['artists_df'].copy()
            x_range = df['nickname'].astype(str).tolist()
            source = ColumnDataSource(df)
            p = figure(x_range=x_range, height=400, title="Топ Артистів", tools="hover", tooltips=[("Артист", "@nickname"), ("Пісень", "@filtered_song_count")])
            p.vbar(x='nickname', top='filtered_song_count', width=0.8, source=source, line_color='white', fill_color="#198754")
            p.xgrid.grid_line_color = None; p.y_range.start = 0
            plots['chart3'] = p
        except Exception as e: debug_log.append(str(e))

    if data and not data['albums_df'].empty:
        try:
            df = data['albums_df'].copy()
            x_range = df['title'].astype(str).tolist()
            source = ColumnDataSource(df)
            p = figure(x_range=x_range, height=400, title="Топ Альбомів", tools="hover", tooltips=[("Альбом", "@title"), ("Треків", "@filtered_track_count")])
            p.vbar(x='title', top='filtered_track_count', width=0.8, source=source, line_color='white', fill_color="#ffc107")
            p.xgrid.grid_line_color = None; p.y_range.start = 0
            plots['chart4'] = p
        except Exception as e: debug_log.append(str(e))

    if data and not data['countries_df'].empty:
        try:
            df = data['countries_df'].copy()
            df['angle'] = df['artist_count'] / df['artist_count'].sum() * 2 * pi
            df['color'] = COLORS[:len(df)]
            source = ColumnDataSource(df)
            p = figure(height=400, title="Топ Країн", toolbar_location=None, tools="hover", tooltips="@country: @artist_count", x_range=(-0.5, 1.0))
            p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color', legend_field='country', source=source)
            p.axis.visible = False; p.grid.grid_line_color = None
            plots['chart5'] = p
        except Exception as e: debug_log.append(str(e))

    if data and not data['producers_df'].empty:
        try:
            df = data['producers_df'].copy()
            x_range = df['nickname'].astype(str).tolist()
            source = ColumnDataSource(df)
            p = figure(x_range=x_range, height=400, title="Топ Продюсерів", tools="hover", tooltips=[("Продюсер", "@nickname"), ("Пісень", "@filtered_prod_count")])
            p.vbar(x='nickname', top='filtered_prod_count', width=0.8, source=source, line_color='white', fill_color="#0dcaf0")
            p.xgrid.grid_line_color = None; p.y_range.start = 0
            plots['chart6'] = p
        except Exception as e: debug_log.append(str(e))

    if plots:
        script, divs = components(plots)
    else:
        script = ""
        divs = {}
    
    bokeh_js = CDN.render()

    context = {
        'script': script, 
        'divs': divs, 
        'bokeh_js': bokeh_js, 
        'debug_log': debug_log,
        'stats': stats, # Додано для виведення статистики
        'filter_type': filter_type, 'min_year': min_year, 'max_year': max_year,
        'all_genres': Song.objects.values_list('genre__name', flat=True).distinct().order_by('genre__name'),
        'all_countries': Artist.objects.exclude(country='').exclude(country__isnull=True).values_list('country', flat=True).distinct().order_by('country'),
        'selected_genre': selected_genre, 'selected_country': selected_country
    }
    return render(request, 'web/dashboard_bokeh.html', context)

def export_dashboard_csv(request):
    filter_type, min_year, max_year, selected_genre, selected_country = _get_filter_params(request)
    
    data = get_aggregated_data(
        min_year=min_year if filter_type == 'year' else None,
        max_year=max_year if filter_type == 'year' else None,
        genre_filter=selected_genre,
        country_filter=selected_country
    )
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="music_analytics_report.csv"'
    
    response.write(u'\ufeff'.encode('utf8'))
    
    writer = csv.writer(response)
    
    writer.writerow(['--- ТОП ЖАНРІВ ---'])
    writer.writerow(['Жанр', 'Кількість пісень'])
    if not data['genres_df'].empty:
        for _, row in data['genres_df'].iterrows():
            writer.writerow([row['genre__name'], row['total_songs']])
    writer.writerow([]) 

    writer.writerow(['--- ДИНАМІКА ПО РОКАХ ---'])
    writer.writerow(['Рік', 'Середня тривалість (хв)'])
    if not data['years_df'].empty:
        for _, row in data['years_df'].iterrows():
            writer.writerow([row['release_year'], row['avg_duration']])
    writer.writerow([])

    writer.writerow(['--- ТОП АРТИСТІВ ---'])
    writer.writerow(['Артист', 'Кількість пісень'])
    if not data['artists_df'].empty:
        for _, row in data['artists_df'].iterrows():
            writer.writerow([row['nickname'], row['filtered_song_count']])
    writer.writerow([])

    writer.writerow(['--- ТОП АЛЬБОМІВ ---'])
    writer.writerow(['Альбом', 'Кількість треків'])
    if not data['albums_df'].empty:
        for _, row in data['albums_df'].iterrows():
            writer.writerow([row['title'], row['filtered_track_count']])
    writer.writerow([])
    
    writer.writerow(['--- ТОП КРАЇН ---'])
    writer.writerow(['Країна', 'Кількість артистів'])
    if not data['countries_df'].empty:
        for _, row in data['countries_df'].iterrows():
            writer.writerow([row['country'], row['artist_count']])
    writer.writerow([])

    return response