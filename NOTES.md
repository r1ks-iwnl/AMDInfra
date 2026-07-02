# Ziua 1
## Tema #1
Fișierele log conțin rezultatele simulărilor de Functional Coverage făcute de Synopsys pentru coverpoint-uri: 
cp_vec, cp_pop, cp_en, cp_vote, x_en_vote

Coverpoint-urile în sine raportează rata de hit/miss pentru diferite combinații de intrări afișând și rezultatele pentru fiecare combinație specifică.

> Data rulării
 
Apare pe linia 1 în fiecare fișier

> Rezultatele generale/coverpoint-uri

Rezultatele generale apar în zona 
```
=========== Functional Coverage ===========
 cp_vec    :  62.50%
 cp_pop    :  80.00%
 cp_en     : 100.00%
 cp_vote   : 100.00%
 x_en_vote :  75.00%
 OVERALL   :  83.50%
 ```

 Iar pentru coverpoint-uri:

 ```
 cp_vec bins  (in3in2in1in0):
   vec[ 0]  0000 : hits=2           HIT
   vec[ 1]  0001 : hits=1           HIT
   vec[ 2]  0010 : hits=1           HIT
   vec[ 3]  0011 : hits=0  *** MISS ***
   vec[ 4]  0100 : hits=7           HIT
   vec[ 5]  0101 : hits=0  *** MISS ***
   vec[ 6]  0110 : hits=2           HIT
   vec[ 7]  0111 : hits=1           HIT
   vec[ 8]  1000 : hits=0  *** MISS ***
   vec[ 9]  1001 : hits=1           HIT
   vec[10]  1010 : hits=0  *** MISS ***
    ...
```

> Forme diferite de tabeluri de bin-uri

```
 vec[ 0]  0000 : hits=2           HIT
```

Testare prin index zecimal tradus in cod binar

```
   none(0) : hits=2           HIT
```
Testare prin numar de intrari setate ca HIGH

```
   en=0   : hits=12           HIT
```
Testare prin valoare HIGH/LOW
```
   (en=0,vote=0) : hits=12           HIT
```
Testare prin combinație de coverpoint-uri 

> Ce distinge o linie HIT de una MISS

Avem o linie MISS atunci când avem 0 hit-uri, HIT dacă există hit-uri.

## Tema #2

> Câte bin-uri sunt în total și câte sunt MISS?

29 bin-uri, 12 MISS

> Se respectă regula 'hits>0 înseamnă HIT' pe fiecare linie?

Da

# Ziua 3

> Un scenariu real în care DB-First bate Code-First

DB-First este superior în cazul proiectelor care implică mai multe persoane și unde se folosesc mai multe limbaje  
pentru că se menține principiul "single source of truth" folosind doar SQL direct evitând fragmentarea schemelor   
folosind limbaje diferite.
