import locale
locale.setlocale(locale.LC_ALL, '')

def coloca_em_template(template_str, lista_substituições):
    for s in lista_substituições:
        template_str = template_str.replace(s[0], str(s[1]))
    return template_str

def f_float(x):
    s = f'{x:,.2f}'
    s = s.replace('.', '*')
    s = s.replace(',', '.')
    s = s.replace('*', ',')
    return s

def f_int(i):
    s = f'{int(i):,d}'
    s = s.replace(',', '.')
    return s

def f_perc(p):
    s = f_float(p) + '%'
    return s

import textwrap
def wrap(texto, largura):
  return '<br>'.join(textwrap.wrap(texto, width=largura))

def normatiza(taxa):
    if taxa == 0.0:
        return 99999 # Alguma coisa está errada.
    numerador = taxa
    denominador = 1
    while numerador < 1:
        numerador *= 10
        denominador *= 10
        #print(f"denominador = {denominador}")
    return denominador