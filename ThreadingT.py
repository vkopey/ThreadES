#encoding: utf-8
"""Розрахунок основного часу на обробку різьб
P - крок різьби, мм;
L - довжина робочого ходу, мм;
L_p - довжина різьби, що нарізується, мм;
y - величина, що враховує підхід, врізання та перебіг, мм;
L_i - ширина інструменту, мм;
d - діаметр різьби, що нарізується, мм;
L_d - інтервал між гайками при нарізанні гайковими мітчиками, мм;
n - частота обертання заготовки або інструменту, хв-1;
n_r - частота обертання заготовки або інструменту на зворотному ході (прискореному) мін-1;
n_z - частота обертання заготовки, хв-1;
n_i - частота обертання інструменту, хв-1;
n_2 - число подвійних ходів за хвилину;
S_z - подача на зуб фрези (на один різець), мм/зуб;
Z - число зубів (різців) інструмента;
i - число робочих ходів інструмента;
g - число заходів різьби, що нарізується;
m - кількість заготовок, що обробляються за один оберт накатного ролика;
n_p - кількість оборотів заготовки під час профілювання різьби при накатуванні;
t_k - час калібрування різьби при накатуванні, хв;
e_i - число заходів інструмента (ролика)
"""

def doc2dict(s):
    """Перетворює в словник текст в форматі:
    key1 - value1
    key2 - value2
    ..."""
    d={}
    for ln in s.splitlines():
        sln=ln.split('-')
        try:
            d[sln[0].strip()]=sln[1].strip()
        except:
            pass
    return d

def extdoc(f, d):
    """Доповнює документацію функції f інформацією про аргументи, якщо вона є в словнику d"""
    from inspect import getfullargspec
    fargs=getfullargspec(f).args
    for arg in fargs:
        argdoc=d.get(arg)
        if argdoc!=None:
            f.__doc__+="\n"+arg+" - "+argdoc

##
def T1(L, P, n):
    """Повертає основний час для нарізання різьби машинним мітчиком, хв"""
    return 2*L/(P*n)

def T2(L, P, n, n_r):
    """Повертає основний час для нарізання різьби машинним мітчиком з прискореним реверсуванням, хв"""
    return (1/n+1/n_r)*L/P

def T3(L_p, L_d, P, n):
    """Повертає основний час для нарізання різьби машинним мітчиком гайковим, хв"""
    return (L_p+L_d)/(P*n)

def T4(L, P, n, n_r):
    """Повертає основний час для нарізання різьби аксіальними головками з реверсуванням, хв"""
    return (1/n+1/n_r)*L/P

def T5(L, P, n):
    """Повертає основний час для нарізання різьби аксіальними головками з розкриттям, хв"""
    return L/(P*n)

def T6(L_p, L_i, P, n):
    """Повертає основний час для нарізання різьби аксіальними головками напрохід, хв"""
    return (L_p+L_i)/(P*n)

def T7(L, P, n, g=1, i=1):
    """Повертає основний час для точіння різьби, хв"""
    return L*i*g/(P*n)

def T8(L, P, S, d, g=1, i=1):
    """Повертає основний час для фрезерування дисковою фрезою, хв"""
    return L*3.14*d*i*g/(P*S)

def T9(d, S_z, Z, n_i):
    """Повертає основний час для фрезерування гребінчастою фрезою, хв"""
    return 1.25*3.14*d/(S_z*Z*n_i)

def T10(n_z):
    """Повертає основний час для шліфування багатонитковим кругом врізне, хв"""
    return 1.65/n_z

def T11(L, P, n_z, i=1):
    """Повертає основний час для шліфування багатонитковим кругом поздовжнє, хв"""
    return 1.4*L*i/(P*n_z)

def T12(L, P, n_z, i=1):
    """Повертає основний час для вихрового нарізання головками з внутрішнім та зовнішнім доторком, хв"""
    return L*i/(P*n_z)

def T13(n_i, m):
    """Повертає основний час для накатування планетарного, хв"""
    return 1/(n_i*m)

def T14(n_2):
    """Повертає основний час для накатування плоскими плашками, хв"""
    return 1/(n_2)

def T15(n, t_k, n_i, e_i, e_z):
    """Повертає основний час для накатування роликами з радіальною подачею, хв"""
    return n/(n_i*e_i/e_z)+t_k

def T16(L_p, L_i, P, n_i, D_2p, d2, e_z):
    """Повертає основний час для накатування роликами з осьовою подачею, хв"""
    return (L_p+L_i)/(n_i*P*e_z*D_2p/d2)

def T17(n_i, m):
    """Повертає основний час для накатування роликами з затилуванням, хв"""
    return 1/(n_i*m)

def T18(n_i, n_z, t_k):
    """Повертає основний час для накатування тангенціальними головками, хв"""
    return n_i/n_z+t_k

##
if __name__=="__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    L=np.arange(0.0, 100, 1)
    P=1
    n=1000
    plt.plot(L, T1(L, P, n), 'r-', lw=2) # label='T1'
    plt.plot(L, T2(L, P, n, 2000), 'k:', lw=2)
    plt.plot(L, T7(L, P, n), 'r--', lw=2)
    plt.plot(L, T8(L, P, 5000, 10), 'k-', lw=2)
    plt.plot(L, T9(10, 0.5, 4, 100)*L/L, 'k--', lw=2) # *P/P потрібне для масиву
    plt.xlabel("L, мм"); plt.ylabel("To, хв");
    plt.legend([f for f in "T1 T2 T7 T8 T9".split()])
    #plt.legend(['$'+fn2latex(f)+'$' for f in (T1,T2,T7,T8,T9)])
    plt.show()
    ##
    L=50
    P=np.arange(1, 5, 0.1)
    plt.plot(P, T1(L, P, n), 'r-', lw=2)
    plt.plot(P, T2(L, P, n, 2000), 'k:', lw=2)
    plt.plot(P, T7(L, P, n), 'r--', lw=2)
    plt.plot(P, T8(L, P, 5000, 10), 'k-', lw=2)
    plt.plot(P, T9(10, 0.5, 4, 100)*P/P, 'k--', lw=2) # *P/P потрібне для масиву
    plt.legend([f for f in "T1 T2 T7 T8 T9".split()])
    plt.xlabel("P, мм"); plt.ylabel("To, хв")
    plt.show()
    ##

    from example2 import *
    # розширити документацію
    for f in [T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16, T17, T18]:
        f.__doc__+="\n\n$$"+fn2latex(f)+"$$\n"
        extdoc(f, doc2dict(__doc__))

    ##
    fn2sympy(T7)
    fn2sympy(T7, P=2)
    fn2latex(T7)
    fndoc(T7)
    T7.__doc__
    fn_solve(T7, 0.1, L=10, P=2, g=1, i=1)
    fn_solve(T7, 0.1, L=10, P=sympy.S("P"), g=1, i=1)

    ##
    eq1=fn2sympy(T7)
    print(eq1)
    eq2=fn2sympy(T9)
    print(eq2)
    sol=sympy.solve(sympy.Eq(eq1.rhs, eq2.rhs), "L")
    print(sol)
    sol=sympy.solve(sympy.Eq(eq1.rhs, eq2.rhs), "P")
    print(sol)