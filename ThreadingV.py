#encoding: utf-8
"Режими різьбонарізання"
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def V1(D=None, P=None, m=None, k1=None, k2=None, HB=None):
    """Швидкість різання машинними мітчиками зі сталі Р6М5 [Якухин, т.38].
    Більше значення треба приймати для різьб з більшими діаметрами і меньшими кроками
    D - діаметр різьби, мм
    P - крок, мм,
    m - матеріал
    k1 - матеріал
    k2 - ступінь точності
    НВ - твердість чавуну
    Приклад:
    V1(5, 1, "Сталь конструкційна", "Сталь нормалізована", 6)
    V1()
    """
    V={"Сталь конструкційна":{(3,6):(8,5), (8,10):(12,6), (12,16):(16,8), (18,27):(18,10),(30,39): (20,10), (42,48):(24,10)},
       "Сталь корозостійка та жароміцна":{(3,6):(5,3),(8,10):(6,4),(12,16):(8,6),(18,27):(10,7)},
       "Чавун":{(3,6):(6,3),(8,10):(8,5),(12,16):(10,6),(18,27):(11,6),(30,39):(12,7)},
       "Кольорові сплави":{(3,6):(10,6),(8,10):(12,8),(12,16):(16,10),(18,27):(18,12),(30,39):(20,14),(42,48):(24,15)},
       "Термореактивні пластмасси":{(3,6):(1,5),(8,10):(1.5,7),(12,16):(2,9),(18,27):(2,12)}}
    K1={"Сталь нормалізована":1,
        "Сталь покращена":0.85,
        "Сталь автоматна":1.15,
        "Сталь маловуглецева":0.825,
        "Сталь легована нормалізована":0.9,
        "Сталь легована покращена":0.7,
        "Сталь корозійно-стійка":0.75,
        "Жароміцні сталі та сплави":0.25,
        "Жаростійкі сталі та сплави":0.25,
        "Бронза":1.0,
        "Латунь":1.2,
        "Алюміній":1.3,
        "Фенопласт та текстолит":1,
        "Склотекстолит":0.5,
        "Чавун сірий":{190:1.0, 210:0.7, 230:0.5},
        "Чавун ковкий":{155:1.5, 170:1.05, 195:0.75} }
    K2={4:0.8, 6:1.0, 8:1.2}
    if all((D, P, m, k1, k2)):
        for D1,D2 in V[m].keys():
            if D1<=D<=D2: D=D1,D2; break
        k1=K1[k1][HB] if HB else K1[k1]
        k2=K2[k2]
        return np.array(V[m][D])*k1*k2
    else:
        return V, K1, K2

def V1pd():
    """Швидкість різання машинними мітчиками зі сталі Р6М5 [Якухин, т.38]
    Використання Pandas.
    Приклади:
    V[V.D==(3,6)]["Сталь конструкційна"]
    V.D[ [i<5<j for i,j in V.D] ]
    V["Сталь конструкційна"][ [i<5<j for i,j in V.D] ]
    """
    # або відразу розбити на стовпчики min,max
    V = {'D': [(3,6),(8,10),(12,16),(18,27),(30,39),(42,48)],
         'P': [(0.5,1),(0.5,1.5),(0.5,2),(0.75,3),(1,3),(1,3)],
         "Сталь конструкційна": [(8,5),(12,6),(16,8),(18,10),(20,10),(24,10)],
         "Сталь корозостійка та жароміцна": [(5,3),(6,4),(8,6),(10,7),(0,0),(0,0)],
         "Чавун": [(6,3),(8,5),(10,6),(11,6),(12,7),(0,0)],
         "Кольорові сплави": [(10,6),(12,8),(16,10),(18,12),(20,14),(24,15)],
         "Термореактивні пластмасси": [(1,5),(1.5,7),(2,9),(2,12),(0,0),(0,0)] }
    V = pd.DataFrame(data=V)
    # створити нові стовпчики min,max
    #V['Dmin']=pd.Series([i for i,j in V.D])
    #V['Dmax']=pd.Series([j for i,j in V.D])
    # і так усі стовпчики...
    # або:
    for c in V.columns:
        V[c+'min']=pd.Series([i for i,j in V[c]])
        V[c+'max']=pd.Series([j for i,j in V[c]])
    return V

# Розрахунок швидкості різання гвинторізними головками з дисковими гребінками та круглими плашками
def V_dcrd(d, P, m, q, phi, K1, K2, K3, k_1, k_2, k_3):
    u"""Розрахунок швидкості різання"""
    V={"P=0.5":{(3,6):(10),(8,10):(12)},
       "P=0.75":{(3,6):(9),(8,10):(12),(12,16):(16),(18,24):(28),(27):(20)},
       "P=1.0":{(3,6):(8),(8,10):(11),(12,16):(16),(18,24):(18),(27):(20)},
       "P=1.25":{(8,10):(11),(12,16):(15),(18,24):(16),(27):(18)},
       "P=1.5":{(8,10):(10),(12,16):(14),(18,24):(15),(27):(16)},
       "P=2.0":{(12,16):(12),(18,24):(13),(27):(14)},
       "P=3.0":{(18,24):(12),(27):(13)}}
    K1={"Сталь нормалізована":1,
        "Сталь покращена":0.85,
        "Сталь автоматна":1.15,
        "Сталь маловуглецева":0.825,
        "Сталь легована нормалізована":0.9,
        "Сталь легована покращена":0.7,
        "Сталь корозійно-стійка":0.75,
        "Жароміцні сталі та сплави":0.25,
        "Жаростійкі сталі та сплави":0.25,
        "Бронза":1.0,
        "Латунь":1.2,
        "Алюміній":1.3,
        "Фенопласт та текстолит":1,
        "Склотекстолит":0.5,
        "Чавун сірий з HB":{(190):(1.0),(210):(0.7),(230):(0,5)},
        "Чавун ковкий з HB":{(155):(1.5),(170):(1.05),(195):(0,75)}},
    K2={"Ступінь точності розміру":{(4):(0.8),(6):(1.0),(8):(1.2)}}
    K3={"Коефіцієнт кута забірного конуса":{(10):(1.4),(20):(1.0),(30):(0.5),(45):(0.25)}}
    return V[P][D]*K1[k_1][m]*K2[k_2][q]*K3[k_3][phi]

# Розрахунок швидкості різання токарним різцем
def V_lcut(P, sigmaV):
    u"""Розрахунок швидкості різання"""
    V={"Різьба зовнішня P=1.5 чорновий та чистовий":{(550,620):(160),(630,700):(142),(710,790):(126),(800,890):(107)},
       "Різьба зовнішня P=3.0 чорновий та чистовий":{(550,620):(141),(630,700):(125),(710,790):(111),(800,890):(94)},
       "Різьба зовнішня P=5.0 чорновий та чистовий":{(550,620):(124),(630,700):(110),(710,790):(98),(800,890):(83)},
       "Різьба внутрішня P=1.5 чорновий та чистовий":{(550,620):(137),(630,700):(121),(710,790):(108),(800,890):(92)},
       "Різьба внутрішня P=3.0 чорновий та чистовий":{(550,620):(113),(630,700):(100),(710,790):(89),(800,890):(76)},
       "Різьба внутрішня P=5.0 чорновий та чистовий":{(550,620):(97),(630,700):(86),(710,790):(77),(800,890):(65)},
       "Різьба зовнішня P=1.5 чистовий":{(550,620):(178),(630,700):(157),(710,790):(140),(800,890):(120)},
       "Різьба зовнішня P=3.0 чистовий":{(550,620):(198),(630,700):(174),(710,790):(155),(800,890):(132)},
       "Різьба зовнішня P=5.0 чистовий":{(550,620):(207),(630,700):(183),(710,790):(163),(800,890):(139)},
       "Різьба внутрішня P=1.5 чистовий":{(550,620):(141),(630,700):(125),(710,790):(112),(800,890):(96)},
       "Різьба внутрішня P=3.0 чистовий":{(550,620):(147),(630,700):(130),(710,790):(116),(800,890):(99)},
       "Різьба внутрішня P=5.0 чистовий":{(550,620):(162),(630,700):(143),(710,790):(127),(800,890):(108)}}
    return V[P][sigmaV]

# Розрахунок швидкості при фрезеруванні та вихровому нарізанні
def V_mill(m_, sigmaV, S, m, d, K1, K2, k_1, k_2):
    u"""Розрахунок швидкості різання"""
    V={"Сталь":{(0.02):(57),(0.03):(48),(0.04):(47),(0.05,0.06):(39),(0.07):(32),(0.1):(22)},
       "Ковкий чавун":{(0.04):(51),(0.05):(47),(0.06):(42),(0.07):(39),(0.09):(32),(0.1):(27),(0.12):(24)},
       "Сірий чавун":{(0.1):(45),(0.12):(37)}}
    K1={"Конструкційна сталь":{(600,700):(1.15),(710,800):(1.0),(810,930):(0.86),(970,1070):(0.66),(1080,1240):(0.49)},
        "Ковкий чавун":{(149,163):(1.0),(172,201):(0.8),(163,229):(0.65)},
        "Сірий чавун":{(143,229):(1.0),(170,255):(0.9),(197,269):(0.8)}}
    K2={"Коефіцієнт діаметру фрези":{(40):(0.9),(60):(1.0),(80):(1.05),(100):(1.1)}}
    return V[S][m_]*K1[k_1][m]*K2[k_2][d]

def V_whr(S, sigmaV):
    u"""Розрахунок швидкості різання"""
    V={"Різьба внутрішня sigmaV=550 при P=3.0":{(1.0):(164),(1.2):(150)},
       "Різьба внутрішня sigmaV=550 при P=5.0":{(1.0):(128),(1.2):(115)},
       "Різьба внутрішня sigmaV=550 при P=8.0":{(1.0):(102),(1.2):(92)},
       "Різьба внутрішня sigmaV=650 при P=3.0":{(0.8):(155),(1.0):(138),(1.2):(127)},
       "Різьба внутрішня sigmaV=650 при P=5.0":{(0.8):(120),(1.0):(107),(1.2):(98)},
       "Різьба внутрішня sigmaV=650 при P=8.0":{(0.8):(95),(1.0):(85),(1.2):(78)},
       "Різьба внутрішня sigmaV=750 при P=3.0":{(0.6):(155),(0.8):(134),(1.0):(120)},
       "Різьба внутрішня sigmaV=750 при P=5.0":{(0.6):(120),(0.8):(104),(1.0):(93)},
       "Різьба внутрішня sigmaV=750 при P=8.0":{(0.6):(95),(0.8):(82),(1.0):(74)},
       "Різьба внутрішня sigmaV=850 при P=3.0":{(0.6):(138),(0.8):(119)},
       "Різьба внутрішня sigmaV=850 при P=5.0":{(0.4):(131),(0.6):(106),(0.8):(92)},
       "Різьба внутрішня sigmaV=850 при P=8.0":{(0.4):(103),(0.6):(85),(0.8):(73)},
       "Різьба зовнішня sigmaV=550 при P=3.0":{(1.0):(205),(1.2):(187)},
       "Різьба зовнішня sigmaV=550 при P=5.0":{(1.0):(159),(1.2):(145)},
       "Різьба зовнішня sigmaV=550 при P=8.0":{(1.0):(126),(1.2):(114)},
       "Різьба зовнішня sigmaV=650 при P=3.0":{(0.8):(194),(1.0):(173),(1.2):(158)},
       "Різьба зовнішня sigmaV=650 при P=5.0":{(0.8):(150),(1.0):(134),(1.2):(123)},
       "Різьба зовнішня sigmaV=650 при P=8.0":{(0.8):(118),(1.0):(116),(1.2):(97)},
       "Різьба зовнішня sigmaV=750 при P=3.0":{(0.6):(194),(0.8):(168),(1.0):(150)},
       "Різьба зовнішня sigmaV=750 при P=5.0":{(0.6):(150),(0.8):(130),(1.0):(116)},
       "Різьба зовнішня sigmaV=750 при P=8.0":{(0.6):(118),(0.8):(103),(1.0):(92)},
       "Різьба зовнішня sigmaV=850 при P=3.0":{(0.4):(209),(0.6):(172),(0.8):(149)},
       "Різьба зовнішня sigmaV=850 при P=5.0":{(0.4):(162),(0.6):(133),(0.8):(115)},
       "Різьба зовнішня sigmaV=850 при P=8.0":{(0.4):(128),(0.6):(106),(0.8):(91)}}
    return V[sigmaV][S]

# Режими різьбонакатування
# Радіальна подача при накатуванні двома роликами
def S_r( P, sigmaV):
    u"""Розрахунок радіальної подачі"""
    S={"Сталь sigmaV=400":{(1.0):(0.045,0.15),(1.5):(0.06,0.17),(2.0):(0.075,0.20),(2.5):(0.08,0.25),(3.0):(0.085,0.26)},
       "Сталь sigmaV=400-500":{(1.0):(0.03,0.1),(1.5):(0.045,0.15),(2.0):(0.045,0.17),(2.5):(0.075,0.23),(3.0):(0.08,0.25)},
       "Сталь sigmaV=550+":{(1.0):(0.025,0.09),(1.5):(0.035,0.12),(2.0):(0.055,0.16),(2.5):(0.06,0.2),(3.0):(0.065,0.23)},
       "Латунь":{(1.0):(0.04,0.17),(1.5):(0.05,0.20),(2.0):(0.06,0.23),(2.5):(0.07,0.27),(3.0):(0.08,0.30)}}
    return S[sigmaV][P]

# Швидкість накатування аксіальними головками
def V_r( m, kind):
    u"""Розрахунок швидкості накатування"""
    V={"Конструкційна сталь sigmaV=700":{(metric):(30,90),(trap):(30)},
       "Конструкційна сталь sigmaV=900":{(metric):(30,60),(trap):(25)},
       "Корозійно стійка сталь":{(metric):(30,50),(trap):(25)},
       "Кольрові сплави":{(metric):(60,90),(trap):(50)}}
    return S[m][kind]

# Швидкість накатування безстружковими мітчиками
def V_tap( P, d, nb, m, m1, k_1, k_2, k_3):
    u"""Розрахунок швидкості накатування"""
    V={"d(1-6)":{(0.2,0.5):(14),(0.6,0.75):(16),(1.0):(18)},
       "d(8-10)":{(0.2,0.5):(16),(0.6,0.75):(18),(1.0):(20),(1.25):(22)},
       "d(12-16)":{(0.2,0.5):(18),(0.6,0.75):(20),(1.0):(22),(1.25):(22),(1.5):(24),(2.0):(24)},
       "d(18-24)":{(0.2,0.5):(20),(0.6,0.75):(22),(1.0):(24),(1.5):(28),(2.0):(28)},
       "d(27)":{(0.6,0.75):(24),(1.0):(26),(1.5):(30),(2.0):(30)}}
    K1={"Коефіцієнт твердості":{(30,70):(1.0),(70,120):(0.85),(120,156):(0.6)}}
    K2={"Коефіцієнт матеріалу заготовки":{(copper):(1.0),(brass):(0.7),(steel):(0.55),(aluminium):(1.4)}}
    K3={"Коефіцієнт матеріалу мітчика":{(P6M5):(1.0),(P18):(1.3),(P9F5):(1.7)}}
    return V[P][d]*K1[k_1][hb]*K2[k_2][m]*K3[k_3][m1]

if __name__=="__main__":
    V=V1pd()
    X=(V['Dmax']+V['Dmin'])/2

    plt.plot(X.values, V['Pmin'].values, 'k-')
    plt.plot(X.values, V['Pmax'].values, 'k-')
    plt.xlabel('D, мм'); plt.ylabel('Pmin, Pmax, мм')
    plt.title("""Залежність мінімального та максимального кроку різьби
від її діаметра під час нарізання машинним мітчиком""")
    plt.show()

    plt.plot(X.values, V['Сталь конструкційнаmin'].values, 'k-')
    plt.plot(X.values, V['Сталь конструкційнаmax'].values, 'k-')
    plt.plot(X.values[:-1], V['Чавунmin'].values[:-1], 'k--')
    plt.plot(X.values[:-1], V['Чавунmax'].values[:-1], 'k--')
    plt.plot(X.values[:-2], V['Термореактивні пластмассиmin'].values[:-2], 'k:')
    plt.plot(X.values[:-2], V['Термореактивні пластмассиmax'].values[:-2], 'k:')
    plt.xlabel('D, мм'); plt.ylabel('Vmin, Vmax м/хв')
    plt.title("""Залежність максимальної і мінімальної швидкості різання від
діаметра різьби для нарізання машинним мітчиком зі сталі Р6М5""")
    plt.text(5,20,"""сталь конструкційна (-)
чавун (- -)
термореактивні пластмаси (...)""")
    plt.show()

    plt.plot(X.values[:-2], V['Сталь корозостійка та жароміцнаmin'].values[:-2], 'k-')
    plt.plot(X.values[:-2], V['Сталь корозостійка та жароміцнаmax'].values[:-2], 'k-')
    plt.plot(X.values, V['Кольорові сплавиmin'].values, 'k--')
    plt.plot(X.values, V['Кольорові сплавиmax'].values, 'k--')
    plt.xlabel('D, мм'); plt.ylabel('Vmin, Vmax, м/хв')
    plt.title("""Залежність максимальної і мінімальної швидкості різання від
діаметра різьби для нарізання машинним мітчиком зі сталі Р6М5""")
    plt.text(5,20,"""сталь корозостійка та жароміцна (-)
кольорові сплави (- -)""")
    plt.show()