meniu = ['papanasi'] * 10 + ['ceafa'] * 3 + ["guias"] * 6
preturi = [["papanasi", 7], ["ceafa", 10], ["guias", 5]]
studenti = ["Liviu", "Ion", "George", "Ana", "Florica"]  # coada FIFO
comenzi = ["guias", "ceafa", "ceafa", "papanasi", "ceafa"]  # coada FIFO
tavi = ["tava"] * 7  # stiva LIFO
istoric_comenzi = []

numar_ceafa_la_inceput=meniu.count("ceafa")
numar_comanda_ceafa=comenzi.count("ceafa")

numar_guias_la_inceput=meniu.count("guias")
numar_comanda_guias=comenzi.count("guias")

numar_papanasi_la_inceput=meniu.count("papanasi")
numar_comanda_papanasi=comenzi.count("papanasi")

while studenti:
    student=studenti.pop(0)
    comanda=comenzi.pop(0)
    print(f"Studentul {student} a comandat {comanda}")
    istoric_comenzi.append([student, comanda])
    tavi.pop()

# print(istoric_comenzi)

numar_papanasi=10
numar_ceafa=3
numar_guias=6
pret_papanasi=preturi[0][1]
pret_ceafa=preturi[1][1]
pret_guias=preturi[2][1]

print(f"S-au comandat {numar_comanda_ceafa} ceafa, {numar_comanda_guias} guias, {numar_comanda_papanasi} papanasi")
print(f"Mai sunt {len(tavi)} tavi")

numar_ceafa_ramas=numar_ceafa_la_inceput-numar_comanda_ceafa
numar_papanasi_ramas=numar_papanasi_la_inceput-numar_comanda_papanasi
numar_guias_ramas=numar_guias_la_inceput-numar_comanda_guias

if numar_ceafa_ramas>0:
    print("Mai este ceafa: True")
else:
    print("Mai este ceafa: False")

if numar_papanasi_ramas>0:
    print("Mai sunt papanasi: True")
else:
    print("Mai sunt papanasi: False")

if numar_guias_ramas>0:
    print("Mai este guias: True")
else:
    print("Mai este guias: False")

total_venit=numar_comanda_guias*pret_guias+numar_comanda_papanasi*pret_papanasi+numar_comanda_ceafa*pret_ceafa
print(total_venit)
mancare_ieftina=[]
for mancare_pret in preturi:
    pret_mancare=mancare_pret[1]
    nume_mancare=mancare_pret[0]
    if pret_mancare <=7:
        mancare_ieftina.append(nume_mancare)
print(mancare_ieftina)