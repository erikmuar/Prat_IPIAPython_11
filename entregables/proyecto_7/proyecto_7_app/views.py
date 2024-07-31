from django.shortcuts import render
from .algoritmo_kmp import kmp_search
import time
import matplotlib.pyplot as plt
import os 
from django.conf import settings



def search_pattern(request):
    context = {}
    if request.method == 'POST':
        text = request.POST.get('text')
        pattern = request.POST.get('pattern')
        
        # Multiplicar el texto por 1000 para aumentar el tiempo de procesamiento
        large_text = text * 1000
        
        # Calcular posiciones y recuento en el texto original
        positions = kmp_search(text, pattern)
        count = len(positions)
        
        # Bucle de 10 veces con texto multiplicado
        start_time_10 = time.time()
        for _ in range(10):
            kmp_search(large_text, pattern)
        end_time_10 = time.time()
        duration_10 = end_time_10 - start_time_10
        
        # Bucle de 100 veces con texto multiplicado
        start_time_100 = time.time()
        for _ in range(100):
            kmp_search(large_text, pattern)
        end_time_100 = time.time()
        duration_100 = end_time_100 - start_time_100
        
        # Bucle de 1000 veces con texto multiplicado
        start_time_1000 = time.time()
        for _ in range(1000):
            kmp_search(large_text, pattern)
        end_time_1000 = time.time()
        duration_1000 = end_time_1000 - start_time_1000
        
        x = [10, 100, 1000]
        y = [duration_10, duration_100, duration_1000]
        plt.plot(x, y, marker='o')
        plt.title('Tiempo de Ejecución del Algoritmo KMP')
        plt.xlabel('Número de Repeticiones')
        plt.ylabel('Tiempo (segundos)')
        plt.grid(True)
        
        
        static_dir = os.path.join(settings.BASE_DIR, 'static', 'proyecto_7_app')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        
        graph_path = os.path.join(static_dir, 'kmp_timing_graph.png')
        plt.savefig(graph_path)
        plt.close()
        
        context = {
            'text': text,
            'pattern': pattern,
            'positions': positions,
            'count': count,
            'duration_10': duration_10,
            'duration_100': duration_100,
            'duration_1000': duration_1000,
            'graph_url': '/static/proyecto_7_app/kmp_timing_graph.png',
        }
        
    return render(request, 'algoritmo.html', context)


def compute_prefix_array(pattern):
    
    m = len(pattern)
    prefix_array = [0] * m
    j = 0  # Longitud del prefijo más largo

    for i in range(1, m):
        while (j > 0 and pattern[i] != pattern[j]):
            j = prefix_array[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        prefix_array[i] = j

    return prefix_array
  

def kmp_search(text, pattern):
   
    n = len(text)
    m = len(pattern)
    prefix_array = compute_prefix_array(pattern)
    result = []
    j = 0  # Índice para el patrón

    for i in range(n):
        while (j > 0 and text[i] != pattern[j]):
            j = prefix_array[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == m:
            result.append(i - m + 1)
            j = prefix_array[j - 1]

    return result

def home(request):
    return render(request,"home.html")

def find(request):
    return render(request,"find.html")

def regex(request):
    return render(request,"regex.html")