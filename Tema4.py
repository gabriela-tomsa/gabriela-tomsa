import random
cuvinte = ["python", "programare", "calculator", "date", "algoritm"]
cuvant_de_ghicit = random.choice(cuvinte)
progres = ["_" for _ in cuvant_de_ghicit]

incercari_ramase = 6
litere_incercate = []

def afisare_progres():
           print("" , "".join(progres))
print("Bine ai venit la jocul spanzuratoarea!")
print("Progresul initial este: " ," ".join(progres))

while "_" in progres and incercari_ramase>0:
    incercari_ramase -=1
    litera = input("Introdu o litera: ").lower()
    print(litera)
    if len(litera)!=1 or not litera.isalpha():
        print("Introdu o litera valida.")
        continue

    if litera in litere_incercate:
        print("Ai incercat deja litera aceasta, introdu o alta litera.")
        continue

    litere_incercate.append(litera)
    if litera in cuvant_de_ghicit:
        print("Felicitari! Ai ghicit o litera.")
        for i in range(len(cuvant_de_ghicit)):
            if litera == cuvant_de_ghicit[i]:
                progres[i] = litera
    else:
        incercari_ramase-=-1
        print(f"Litera nu se afla in cuvant. Mai ai {incercari_ramase} incercari.")
    print("Progresul este: " , " ".join(progres))

    afisare_progres()
if incercari_ramase==0:
        print(f"Ai pierdut! Cuvantul era: {cuvant_de_ghicit}")
else:
        print(f"Felicitari! Ai ghicit cuvantul, {''.join(progres)}")
