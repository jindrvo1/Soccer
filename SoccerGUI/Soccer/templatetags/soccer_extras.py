from django import template
from django.utils.safestring import mark_safe
from trueskill import Rating
import numpy as np

register = template.Library()

@register.filter(name="join")
def join(list_data, join_by=", "):
    return f"{join_by}".join([str(x) for x in list_data])

@register.filter(name='get')
def get(data, key):
    if isinstance(data, dict) and key in data:
        return data.get(key)
    elif isinstance(data, tuple) or isinstance(data, list):
        return data[key]
    elif isinstance(data, Rating):
        if key == 'mu':
            return data.mu
        elif key == 'sigma':
            return data.sigma

@register.filter(name='get_last')
def get_last(data):
    if isinstance(data, dict) and len(data.values()) > 0:
        return data[max(data.keys())]
    elif isinstance(data, list) and len(data) > 0:
        return data[-1]

@register.filter(name='wlratiocolor')
def wlratiocolor(ratio):
    if float(ratio) > 50.0:
        ret = f'<span class="green">{ratio} %</span>'
    elif float(ratio) < 50.0:
        ret = f'<span class="red">{ratio} %</span>'
    else:
        ret = f'{ratio} %'
    
    return mark_safe(ret)

@register.filter(name='binarytoyesno')
def binarytoyesno(data):
    if data == 1:
        return "Správně."
    else:
        return "Hm, blbě."

@register.filter(name='round')
def round(data, decimals):
    if isinstance(data, list):
        return [round(x, decimals) for x in data]
    else:
        return np.around(float(data), decimals)

@register.filter(name='topercent')
def topercent(x, decimals):
    return mark_safe('{} %'.format(np.around(float(x)*100, decimals)))

@register.simple_tag(name='winlosecolor')
def winlosecolor(text, score1, score2):
    ret = str(text)

    if int(score1) > int(score2):
        ret = '<span class="green">'+ret+'</span>'
    elif int(score1) < int(score2):
        ret = '<span class="red">'+ret+'</span>'

    return mark_safe(ret)

@register.simple_tag(name='calc_cse')
def calc_cse(arg, sigma=None):
    mu, sigma = (arg.mu, arg.sigma) if sigma is None else (arg, sigma)

    return mu-3*sigma

@register.simple_tag(name='calc_winratio')
def calc_winratio(total, won):
    return 100*won/total

@register.simple_tag(name='higher_streak')
def higher_streak(streaks):
    if streaks[0] > streaks[1]:
        ret = f'<span class="green">{streaks[0]} (W)</span>'
    elif streaks[0] < streaks[1]:
        ret = f'<span class="red">{streaks[1]} (L)</span>'
    else:
        ret = f'{streaks[0]}'

    return mark_safe(ret)

@register.simple_tag(name='mean')
def mean(data):
    return np.mean([float(x) for x in data])

@register.simple_tag(name='mean2args')
def mean2args(x, y):
    return np.mean([
            np.mean([float(z) for z in x]),
            np.mean([float(z) for z in y])
    ])