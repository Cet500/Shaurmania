# Работа с представлениями

## Функциональные представления

Проект использует функциональные представления, организованные по модулям.

### Структура

```python
# main/views/catalog.py
from django.shortcuts import render, get_object_or_404
from main.models import Shaurma

def catalog(request):
    shaurmas = Shaurma.objects.filter(is_available=True)
    return render(request, 'main/catalog.jinja', {'shaurmas': shaurmas})
```

### Группировка по модулям

```
main/views/
├── catalog.py    # Каталог товаров
├── auth.py       # Авторизация
├── profile.py    # Профили
└── ...
```

## Обработка запросов

### GET запросы

```python
def catalog(request):
    category = request.GET.get('category')
    search = request.GET.get('search')
    
    shaurmas = Shaurma.objects.filter(is_available=True)
    
    if category:
        shaurmas = shaurmas.filter(category__slug=category)
    
    if search:
        shaurmas = shaurmas.filter(name__icontains=search)
    
    return render(request, 'main/catalog.jinja', {'shaurmas': shaurmas})
```

### POST запросы

```python
from django.shortcuts import redirect
from django.contrib import messages

def add_to_cart(request, shaurma_id):
    if request.method == 'POST':
        shaurma = get_object_or_404(Shaurma, id=shaurma_id)
        # Логика добавления в корзину
        messages.success(request, 'Товар добавлен в корзину')
        return redirect('cart')
    return redirect('catalog')
```

## Работа с объектами

### get_object_or_404

Используйте `get_object_or_404` вместо `get`:

```python
# Плохо
try:
    shaurma = Shaurma.objects.get(slug=slug)
except Shaurma.DoesNotExist:
    return HttpResponseNotFound()

# Хорошо
shaurma = get_object_or_404(Shaurma, slug=slug, is_available=True)
```

### Оптимизация запросов

```python
# Плохо (N+1 запрос)
shaurmas = Shaurma.objects.all()
# В шаблоне: shaurma.category.name - отдельный запрос для каждой

# Хорошо (1 запрос)
shaurmas = Shaurma.objects.select_related('category').all()
```

## Формы

### ModelForm

```python
# main/forms.py
from django import forms
from main.models import Shaurma

class ShaurmaForm(forms.ModelForm):
    class Meta:
        model = Shaurma
        fields = ['name', 'category', 'price', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }
```

### Использование в представлении

```python
from main.forms import ShaurmaForm

def create_shaurma(request):
    if request.method == 'POST':
        form = ShaurmaForm(request.POST, request.FILES)
        if form.is_valid():
            shaurma = form.save()
            return redirect('product', slug=shaurma.slug)
    else:
        form = ShaurmaForm()
    
    return render(request, 'main/create_shaurma.jinja', {'form': form})
```

### Валидация форм

```python
class MyForm(forms.Form):
    name = forms.CharField(max_length=100)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError('Имя слишком короткое')
        return name
```

## Декораторы

### login_required

```python
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'main/profile.jinja')
```

### user_passes_test

```python
from django.contrib.auth.decorators import user_passes_test

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def admin_view(request):
    return render(request, 'admin/view.jinja')
```

## Обработка ошибок

### Кастомные обработчики

```python
# main/views/errors.py
from django.shortcuts import render

def error_404(request, exception):
    return render(request, 'main/404.jinja', status=404)

def error_500(request):
    return render(request, 'main/500.jinja', status=500)
```

### Регистрация в urls.py

```python
# Shaurmania/urls.py
handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'
```

## Контекстные процессоры

Создавайте контекстные процессоры для глобальных данных:

```python
# main/context_processors.py
def feature_flags(request):
    return {
        'IS_HALLOWEEN': settings.IS_HALLOWEEN,
        'IS_NEW_YEAR': settings.IS_NEW_YEAR,
    }
```

Регистрация в settings.py:

```python
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            'main.context_processors.feature_flags',
        ],
    },
}]
```

## Пагинация

```python
from django.core.paginator import Paginator

def catalog(request):
    shaurmas = Shaurma.objects.filter(is_available=True)
    paginator = Paginator(shaurmas, 20)  # 20 на страницу
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'main/catalog.jinja', {'page_obj': page_obj})
```

## JSON ответы

```python
from django.http import JsonResponse

def api_view(request):
    data = {
        'status': 'success',
        'items': list(Shaurma.objects.values('id', 'name', 'price'))
    }
    return JsonResponse(data)
```

## Лучшие практики

1. **Используйте get_object_or_404** вместо try/except
2. **Оптимизируйте запросы** с select_related/prefetch_related
3. **Группируйте представления** по модулям
4. **Используйте формы** для обработки данных
5. **Обрабатывайте ошибки** кастомными обработчиками
6. **Используйте декораторы** для проверки прав доступа
7. **Минимизируйте логику** в представлениях (выносите в сервисы)

