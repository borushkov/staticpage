from django import template

register = template.Library()


CENSOR_WORDS = ['текст', 'второй', 'редиска', 'плохой']  

@register.filter
def censor(value):
  
    if not isinstance(value, str):
        return value
    
    result = value.split()
 
    for k in range(len(result)):
            if result[k].lower() in CENSOR_WORDS:
                result[k] = result[k][0] + ('*' * (len(result[k])-1))
    return  " ".join(result)
            
    
    