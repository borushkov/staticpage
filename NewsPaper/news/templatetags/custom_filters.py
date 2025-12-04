from django import template

register = template.Library()

# Список слов для цензуры (лучше использовать константу в верхнем регистре)
CENSOR_WORDS = ['текст', 'второй', 'редиска', 'плохой']  # ← исправлено имя

@register.filter
def censor(value):
    """
    Фильтр для цензурирования слов.
    """
    # Проверяем, что значение - строка
    if not isinstance(value, str):
        return value
    
    result = value.split()
    # Проходим по всем словам для цензуры
    for k in range(len(result)):
            if result[k].lower() in CENSOR_WORDS:
                result[k] = result[k][0] + ('*'* (len(result[k])-1))
    return  " ".join(result)
            
    
    