import asyncio
import ssl
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import certifi
import httpx
from asgiref.sync import sync_to_async
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .models import Note, ExternalBook
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from .forms import NoteForm, LoginForm, RegisterForm
from datetime import timedelta
from datetime import datetime
import time
from django.views import View
import requests


def hello_notes(request):
    return HttpResponse("Hello from Notes app.")

def notes_view(request):
    notes = [
        {
            'title': 'Купити продукти',
            'items': ['Молоко', 'Хліб', 'Яйця', 'Смаколики']
        },
        {
            'title': 'Навчання',
            'items': ['Зробити завдання по темі: HTML, CSS', 'Зробити завдання по темі: Мультипроцесорність']
        },
        {
            'title': 'Спорт',
            'items': ['Зробити ранкову пробіжку', 'Відвезти доньку на акробатику']
        },
    ]
    return render(request, 'index.html', {'notes': notes})

def notes_list(request):
    notes = Note.objects.all()
    return render(request, 'notes_list.html', {'notes': notes})

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('list_notes')

class NoteListView(ListView):
    model = Note
    template_name = 'list_notes.html'
    context_object_name = 'notes'
    pk_url_kwarg = 'note_id'
    paginate_by = 10

    def get_queryset(self):
        queryset = Note.objects.select_related('category')
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                title__icontains=search_query)

        return queryset

class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_detail.html'
    context_object_name = 'note'
    pk_url_kwarg = 'note_id'

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    context_object_name = 'note'
    pk_url_kwarg = 'note_id'
    success_url = reverse_lazy('list_notes')


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    context_object_name = 'note'
    pk_url_kwarg = 'note_id'
    success_url = reverse_lazy('list_notes')

def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Вітаємо, {username}')
                return redirect('list_notes')
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна')
            return redirect('list_notes')
        return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Ви вийшли з системи')
    return redirect('login')


class SyncBookImportView(View):
    def get(self, request):
        return render(request, 'book_import.html', {'view_type': 'sync'})

    def post(self, request):
        start_time = time.time()
        isbn_list = [
            '9780545010221',  # Harry Potter
            '9780061120084',  # To Kill a Mockingbird
            '9780451524935',  # 1984
            '9780007123209',  # The Hobbit
            '9780316769174',  # The Catcher in the Rye
            '9780385490818',  # The Da Vinci Code
            '9780553296983',  # Dune
            '9780141439518',  # Pride and Prejudice
            '9780439708180',  # The Hunger Games
            '9780062315007',  # The Alchemist
        ]
        results = []
        errors = []

        for isbn in isbn_list:
            try:
                response = requests.get(
                    f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data',
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    book_key = f"ISBN:{isbn}"
                    if book_key in data:
                        book_data = data[book_key]
                        external_book, created = ExternalBook.objects.get_or_create(
                            external_id=isbn,
                            defaults={
                                'title': book_data.get('title', 'unknown title'),
                                'author_name': ', '.join([author.get('name', 'Unknown') for author in book_data.get('authors', [])]),
                                'description': book_data.get('subtitle', ''),
                                'isbn': isbn
                            }
                        )
                        results.append({
                            'isbn': isbn,
                            'title': external_book.title,
                            'created': created
                        })
                    else:
                        errors.append(f'Книга з ISBN: {isbn} не знайдена!')
                else:
                    errors.append(f'Помилка АПІ для ISBN: {isbn}: {response.status_code}')

            except requests.RequestException as e:
                errors.append(f'Помилка АПІ для ISBN: {isbn}:  {str(e)}')
        end_time = time.time()
        execution_time = end_time - start_time

        return JsonResponse({
            'success': True,
            'execution_time': round(execution_time, 2),
            'results_count': len(results),
            'errors_count': len(errors),
            'results': results,
            'errors': errors,
            'type': 'sync'
        })


class AsyncBookImportView(View):
    async def get(self, request):
        return render(request, 'book_import.html', {'view_type': 'async'})

    async def post(self, request):
        start_time = time.time()
        isbn_list = [
            '9780545010221',  # Harry Potter
            '9780061120084',  # To Kill a Mockingbird
            '9780451524935',  # 1984
            '9780007123209',  # The Hobbit
            '9780316769174',  # The Catcher in the Rye
            '9780385490818',  # The Da Vinci Code
            '9780553296983',  # Dune
            '9780141439518',  # Pride and Prejudice
            '9780439708180',  # The Hunger Games
            '9780062315007',  # The Alchemist
        ]
        results = []
        errors = []
        async def fetch_book(session, isbn):
            try:
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                url = f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data'
                async with session.get(url, timeout=10, ssl=ssl_context) as response:
                    if response.status == 200:
                        data = await response.json()
                        book_key = f"ISBN:{isbn}"
                        if book_key in data:
                            book_data = data[book_key]
                            external_book, created = await sync_to_async(ExternalBook.objects.get_or_create)(
                                external_id=isbn,
                                defaults={
                                    'title': book_data.get('title', 'unknown title'),
                                    'author_name': ', '.join(
                                        [author.get('name', 'Unknown') for author in book_data.get('authors', [])]),
                                    'description': book_data.get('subtitle', ''),
                                    'isbn': isbn
                                }
                            )
                            return {
                                'isbn': isbn,
                                'title': external_book.title,
                                'created': created
                            }
                        else:
                            return {'error': f'Книга з ISBN: {isbn} не знайдена!'}
                    else:
                        return {'error': f'Помилка АПІ для ISBN: {isbn}: {response.status}'}


            except Exception as e:
                return {'error': f'Помилка АПІ для ISBN: {isbn}: {str(e)}'}

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_book(session, isbn) for isbn in isbn_list]
            responses = await asyncio.gather(*tasks)

        for response in responses:
            if 'error' in response:
                errors.append(response['error'])
            else:
                results.append(response)

        end_time = time.time()
        execution_time = end_time - start_time

        return JsonResponse({
            'success': True,
            'execution_time': round(execution_time, 2),
            'results_count': len(results),
            'errors_count': len(errors),
            'results': results,
            'errors': errors,
            'type': 'async'
        })


class HttpClientComparisonView(View):
    """View для порівняння різних HTTP-клієнтів"""

    async def get(self, request):
        return render(request, 'http_comparison.html')

    async def post(self, request):
        client_type = request.POST.get('client_type', 'requests')

        isbn_list = [
            '9780545010221', '9780061120084', '9780451524935',
            '9780007123209', '9780316769174'
        ]

        start_time = time.time()

        if client_type == 'requests':
            results = await self._test_requests(isbn_list)
        elif client_type == 'httpx_sync':
            results = await self._test_httpx_sync(isbn_list)
        elif client_type == 'httpx_async':
            results = await self._test_httpx_async(isbn_list)
        elif client_type == 'aiohttp':
            results = await self._test_aiohttp(isbn_list)
        elif client_type == 'requests_threading':
            results = await self._test_requests_threading(isbn_list)

        end_time = time.time()
        execution_time = end_time - start_time

        return JsonResponse({
            'client_type': client_type,
            'execution_time': round(execution_time, 2),
            'results_count': len(results),
            'results': results
        })

    async def _test_requests(self, isbn_list):
        """Тестування з requests (синхронно) - обгорнуто в sync_to_async"""

        def sync_requests():
            results = []
            for isbn in isbn_list:
                try:
                    response = requests.get(
                        f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data',
                        timeout=5
                    )
                    if response.status_code == 200:
                        results.append({'isbn': isbn, 'status': 'success'})
                    else:
                        results.append({'isbn': isbn, 'status': 'error'})
                except:
                    results.append({'isbn': isbn, 'status': 'error'})
            return results

        return await sync_to_async(sync_requests)()

    async def _test_httpx_sync(self, isbn_list):
        """Тестування з httpx (синхронно) - обгорнуто в sync_to_async"""

        def sync_httpx():
            results = []
            with httpx.Client(timeout=5) as client:
                for isbn in isbn_list:
                    try:
                        response = client.get(
                            f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data'
                        )
                        if response.status_code == 200:
                            results.append({'isbn': isbn, 'status': 'success'})
                        else:
                            results.append({'isbn': isbn, 'status': 'error'})
                    except:
                        results.append({'isbn': isbn, 'status': 'error'})
            return results

        return await sync_to_async(sync_httpx)()

    async def _test_httpx_async(self, isbn_list):
        """Тестування з httpx (асинхронно)"""
        results = []
        async with httpx.AsyncClient(timeout=5) as client:
            async def fetch_isbn(isbn):
                try:
                    response = await client.get(
                        f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data'
                    )
                    if response.status_code == 200:
                        return {'isbn': isbn, 'status': 'success'}
                    else:
                        return {'isbn': isbn, 'status': 'error'}
                except:
                    return {'isbn': isbn, 'status': 'error'}

            tasks = [fetch_isbn(isbn) for isbn in isbn_list]
            results = await asyncio.gather(*tasks)
        return results

    async def _test_aiohttp(self, isbn_list):
        """Тестування з aiohttp (асинхронно)"""
        results = []
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(5)) as session:
            async def fetch_isbn(isbn):
                try:
                    async with session.get(
                            f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data'
                    ) as response:
                        if response.status == 200:
                            return {'isbn': isbn, 'status': 'success'}
                        else:
                            return {'isbn': isbn, 'status': 'error'}
                except:
                    return {'isbn': isbn, 'status': 'error'}

            tasks = [fetch_isbn(isbn) for isbn in isbn_list]
            results = await asyncio.gather(*tasks)
        return results

    async def _test_requests_threading(self, isbn_list):
        """Тестування з requests + threading"""

        def fetch_isbn(isbn):
            try:
                response = requests.get(
                    f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data',
                    timeout=5
                )
                if response.status_code == 200:
                    return {'isbn': isbn, 'status': 'success'}
                else:
                    return {'isbn': isbn, 'status': 'error'}
            except:
                return {'isbn': isbn, 'status': 'error'}

        # Виконання в окремому потоці для уникнення блокування
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = await loop.run_in_executor(
                executor,
                lambda: list(map(fetch_isbn, isbn_list))
            )
        return results