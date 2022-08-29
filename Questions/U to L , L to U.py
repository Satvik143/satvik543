def upper (v):
    v = w.upper()
    print(v)

def lower (v):
    v = w.lower()
    print(v)

w = input("Enter Word : ")

i = input(f"Do You Want To Make {w} Upper Case Or Lower Case : ")

if i == 'upper' or 'UPPER' or 'Upper':
    upper(w)
elif i == 'lower' or 'LOWER' or 'Lower':
    lower(w)