import sqlite3
from django.shortcuts import render, redirect
from django.http import HttpResponse # Por si necesitas hacer pruebas rápidas

def iniciar_desafio(request, desafio_slug):
    if desafio_slug == 'sql-injection':
        # Cambia la llamada directa por un redirect para limpiar la pila de ejecución
        return redirect('sql_challenge') 
    
    return redirect('dashboard')
    
def desafio_sql_injection(request):
    results = []
    error = None
    raw_query = "" # Inicializar como string vacío en lugar de None

    # 1. Creamos la conexión
    conn = sqlite3.connect(':memory:') 
    
    try:
        cursor = conn.cursor()
        
        # 2. Setup de la tabla
        cursor.execute('CREATE TABLE users (id INT, username TEXT, secret_key TEXT)')
        cursor.execute("INSERT INTO users VALUES (1, 'admin', 'FLAG{SQL_MASTER_2024}')")
        cursor.execute("INSERT INTO users VALUES (2, 'operador', 'password123')")
        
        query_input = request.GET.get('q', '')

        if query_input:
            raw_query = f"SELECT username FROM users WHERE username = '{query_input}'"
            cursor.execute(raw_query)
            # 3. Importante: Forzamos la extracción de datos antes de cerrar la conexión
            results = list(cursor.fetchall()) 
            
    except Exception as e:
        error = str(e)
    finally:
        # 4. Cerramos la conexión SIEMPRE, pero después de haber guardado los datos en 'results'
        conn.close() 

    # 5. Renderizado
    return render(request, 'desafios/sql_lab.html', {
        'results': results,
        'error': error,
        'query_ejecutada': raw_query 
    })