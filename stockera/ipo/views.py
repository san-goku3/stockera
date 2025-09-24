# ipo/views.py
from django.shortcuts import render
from django.db import connection
from django.conf import settings
from datetime import datetime

def ipo(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin_app_ipoinfo;")
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for item in data:
            item['company_logo_path'] = f"{settings.MEDIA_URL}{item['company_logo_path']}"
            #item['rhp'] = f"{settings.MEDIA_URL}company_documents/{item['rhp']}"
            #item['drhp'] = f"{settings.MEDIA_URL}company_documents/{item['drhp']}"
            if item['open']:
                try:
                    item['open'] = datetime.strptime(item['open'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                except ValueError:
                    item['open'] = datetime.strptime(item['open'], '%Y-%m-%d').strftime('%Y-%m-%d')
    
            if item['close']:
                try:
                    item['close'] = datetime.strptime(item['close'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                except ValueError:
                    item['close'] = datetime.strptime(item['close'], '%Y-%m-%d').strftime('%Y-%m-%d')

            if item['listing_date']:
                try:
                    item['listing_date'] = datetime.strptime(item['listing_date'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                except ValueError:
                    item['listing_date'] = datetime.strptime(item['listing_date'], '%Y-%m-%d').strftime('%Y-%m-%d')

        print(data)
    return render(request, 'index.html', {'ipo_infos': data})

def upcomming(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin_app_ipoinfo ORDER BY listing_date DESC NULLS LAST LIMIT 10;")
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for item in data:
            item['company_logo_path'] = f"{settings.MEDIA_URL}{item['company_logo_path']}"
            #item['rhp'] = f"{settings.MEDIA_URL}company_documents/{item['rhp']}"
            #item['drhp'] = f"{settings.MEDIA_URL}company_documents/{item['drhp']}"
            if item['open']:
                try:
                    item['open'] = datetime.strptime(item['open'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                except ValueError:
                    item['open'] = datetime.strptime(item['open'], '%Y-%m-%d').strftime('%Y-%m-%d')
    
            if item['close']:
                try:
                    item['close'] = datetime.strptime(item['close'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                except ValueError:
                    item['close'] = datetime.strptime(item['close'], '%Y-%m-%d').strftime('%Y-%m-%d')

            if item['listing_date']:
                try:
                    item['listing_date'] = datetime.strptime(item['listing_date'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                except ValueError:
                    item['listing_date'] = datetime.strptime(item['listing_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
                    
        print(data)
    return render(request, 'upcomming.html', {'ipo_infos': data})
