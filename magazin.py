import json
import random
import copy

def citeste_datele_din_json(fisier):
    with open(fisier, 'r') as f:
        return json.load(f)

def calculeaza_rest(rest, bancnote):
    INF = float('inf')
    dp = [INF] * (rest + 1)
    dp[0] = 0
    combinatii = [{} for _ in range(rest + 1)]

    for valoare, stoc in bancnote:
        for r in range(rest, -1, -1):
            for k in range(1, stoc + 1):
                suma = r + valoare * k
                if suma > rest:
                    break
                if dp[r] + k < dp[suma]:
                    dp[suma] = dp[r] + k
                    combinatii[suma] = combinatii[r].copy()
                    combinatii[suma][valoare] = combinatii[suma].get(valoare, 0) + k

    if dp[rest] == INF:
        return None
    return combinatii[rest]

def actualizeaza_stoc(bancnote, combinatia):
    for i, (valoare, stoc) in enumerate(bancnote):
        if valoare in combinatia:
            bancnote[i] = (valoare, stoc - combinatia[valoare])

def simuleaza_casa(json_path):
    date = citeste_datele_din_json(json_path)
    produse = date['produse']
    bancnote_dict = date['bancnote']
    bancnote = [(b['valoare'], b['stoc']) for b in bancnote_dict]

    client = 1
    while True:
        produs = random.choice(produse)
        pret = produs['pret']
        plata = random.randint(pret + 1, pret + 20)
        rest = plata - pret

        print(f"\nClientul {client}:")
        print(f"  Produs cumpărat: {produs['nume']}")
        print(f"  Preț: {pret} lei")
        print(f"  Suma plătită: {plata} lei")
        print(f"  Rest de oferit: {rest} lei")

        combinatia = calculeaza_rest(rest, bancnote)

        if combinatia is None:
            print("\n NU se poate oferi restul cu bancnotele disponibile!")
            print(f"Rest rămas: {rest} lei")
            print("Stoc actual:")
            for valoare, stoc in bancnote:
                print(f"  {valoare} lei - {stoc} bucăți")
            break
        else:
            print("  Rest oferit cu bancnote:")
            for v, c in sorted(combinatia.items(), reverse=True):
                print(f"    {v} lei x {c}")
            actualizeaza_stoc(bancnote, combinatia)
            client += 1
    print(len(bancnote))
simuleaza_casa('date.json')