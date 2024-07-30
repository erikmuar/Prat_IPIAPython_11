from django.shortcuts import render
from .algoritmo_kmp import kmp_search
import time

def search_pattern(request):
    context = {}
    if request.method == 'POST':
        text = request.POST.get('text')
        pattern = request.POST.get('pattern')
        large_text = text * 1000
        start_time = time.time()  
        
        for _ in range(100): # Hacemos un bucle para que repita la busqueda 100 veces y ver cuanto tarda
            positions = kmp_search(large_text, pattern)
        end_time = time.time()  
        duration = end_time - start_time
        positions = kmp_search(text, pattern)
        count = len(positions)
        positions = kmp_search(text, pattern)
        

        context = {
            'text': text,
            'pattern': pattern,
            'positions': positions,
            'count': count,
            'duration':duration,
        }
    return render(request, 'algoritmo.html', context)


def compute_prefix_array(pattern):
    """Computa el array de prefijos (tabla de fallos) para el patrón."""
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