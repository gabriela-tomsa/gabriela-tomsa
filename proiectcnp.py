import random
import csv
import time
import tkinter as tk
from tkinter import filedialog, ttk
from collections import defaultdict

# Tabel hash pentru stocarea CNP-urilor
hash_table = [[] for _ in range(1009)]  # 1009 este un număr prim pentru a evita coliziunile


def generate_cnp():
    year = random.randint(1900, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 30)
    county = random.choice([x for x in range(1, 53) if x not in [47, 48, 49, 50, 51]])
    unique_id = random.randint(100, 999)
    control_digit = random.randint(0, 9)

    if year >= 2000:
        gender = random.choice([5, 6])
    elif year >= 1900:
        gender = random.choice([1, 2])
    else:
        gender = random.choice([3, 4])

    cnp = f"{gender}{str(year)[-2:]}{month:02}{day:02}{county:02}{unique_id}{control_digit}"
    return cnp


def generate_name():
    """Generează un nume aleatoriu."""
    first_names = ["Andrei", "Maria", "Ion", "Elena", "Alex", "Diana", "Cristian", "Ana"]
    last_names = ["Popescu", "Ionescu", "Dumitrescu", "Stoica", "Georgescu", "Radu"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def hash_function(cnp):
    """Funcția de hash: folosește suma cifrelor CNP-ului modulo 1009."""
    return sum(int(digit) for digit in cnp) % 1009


def insert_in_hash_table(cnp):
    """Inseră un CNP în tabelul hash."""
    index = hash_function(cnp)
    hash_table[index].append(cnp)


def generate_csv(file_name, count=1000000):
    """Generează un fișier CSV cu CNP-uri și nume."""
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["CNP", "Nume"])
        for _ in range(count):
            cnp = generate_cnp()
            name = generate_name()
            writer.writerow([cnp, name])
            insert_in_hash_table(cnp)


def analyze_population(file_name):
    """Analizează distribuția populației după județ, vârstă și sex."""
    county_names = {
        1: "Alba", 2: "Arad", 3: "Argeș", 4: "Bacău", 5: "Bihor", 6: "Bistrița-Năsăud", 7: "Botoșani",
        8: "Brașov", 9: "Brăila", 10: "Buzău", 11: "Caraș-Severin", 12: "Cluj", 13: "Constanța", 14: "Covasna",
        15: "Dâmbovița", 16: "Dolj", 17: "Galați", 18: "Gorj", 19: "Harghita", 20: "Hunedoara", 21: "Ialomița",
        22: "Iași", 23: "Ilfov", 24: "Maramureș", 25: "Mehedinți", 26: "Mureș", 27: "Neamț", 28: "Olt",
        29: "Prahova", 30: "Satu Mare", 31: "Sălaj", 32: "Sibiu", 33: "Suceava", 34: "Teleorman", 35: "Timiș",
        36: "Tulcea", 37: "Vaslui", 38: "Vâlcea", 39: "Vrancea", 40: "București", 41: "București S.1",
        42: "București S.2", 43: "București S.3", 44: "București S.4", 45: "București S.5", 46: "București S.6",
        51: "Călărași", 52: "Giurgiu"
    }
    county_distribution = defaultdict(int)
    age_0_14 = 0
    age_14_18 = 0
    age_18_40 = 0
    age_40_122 = 0
    male_count = 0
    female_count = 0

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            cnp = row[0]
            year = int(cnp[1:3])
            county = int(cnp[7:9])
            gender = int(cnp[0])

            # Determinarea anului complet
            if gender in [1, 2]:
                year += 1900
            elif gender in [5, 6]:
                year += 2000

            age = 2022 - year
            county_distribution[county] += 1

            if 0 <= age < 14:
                age_0_14 += 1
            elif 14 <= age < 18:
                age_14_18 += 1
            elif 18 <= age < 40:
                age_18_40 += 1
            elif 40 <= age <= 122:
                age_40_122 += 1

            if gender in [1, 5]:
                male_count += 1
            elif gender in [2, 6]:
                female_count += 1

    print("Distribuția pe județe:")
    for county, count in sorted(county_distribution.items()):
        print(f"{county_names.get(county, 'Necunoscut')}: {count} persoane")

    print("Distribuția pe categorii de vârstă:")
    print(f"Persoane cu vârsta între 0-14 ani: {age_0_14}")
    print(f"Persoane cu vârsta între 14-18 ani: {age_14_18}")
    print(f"Persoane cu vârsta între 18-40 ani: {age_18_40}")
    print(f"Persoane cu vârsta între 40-122 ani: {age_40_122}")
    print(f"Număr bărbați: {male_count}")
    print(f"Număr femei: {female_count}")


def search_in_hash_table(cnp):
    """Căutare secvențială într-un tabel hash pentru a găsi CNP-ul."""
    index = hash_function(cnp)
    bucket = hash_table[index]
    iterations = 0
    for item in bucket:
        iterations += 1
        if item == cnp:
            return iterations
    return iterations  # Returnăm numărul de iterații (dacă nu se găsește, iterează pe toată lista)


def analyze_search_performance(count=1000):
    """Analizează performanța căutărilor a 1000 de CNP-uri."""
    search_iterations = []

    # Selectăm 1000 de CNP-uri care au fost deja inserate în tabelul hash
    all_cnp_list = []
    for bucket in hash_table:
        all_cnp_list.extend(bucket)  # Adăugăm toate CNP-urile din tabelul hash în listă

    # Verificăm dacă avem suficient de multe CNP-uri pentru a selecta 1000
    if len(all_cnp_list) < count:
        print(f"Numărul de CNP-uri inserate în tabel este mai mic decât {count}.")
        return

    # Selectăm aleatoriu 1000 de CNP-uri din tabelul hash
    selected_cnp = random.sample(all_cnp_list, count)

    # Măsurăm numărul de iterații necesar pentru fiecare căutare
    for cnp in selected_cnp:
        iterations = search_in_hash_table(cnp)
        search_iterations.append(iterations)

    # Calculăm statistici relevante
    avg_iterations = sum(search_iterations) / count
    max_iterations = max(search_iterations)
    min_iterations = min(search_iterations)

    print(f"\nPerformanța căutărilor (pentru 1000 de CNP-uri):")
    print(f"Media numărului de iterații: {avg_iterations:.2f}")
    print(f"Maximul numărului de iterații: {max_iterations}")
    print(f"Minimul numărului de iterații: {min_iterations}")


def main():
    file_name = "cnp_data.csv"
    print("Generare CSV...")
    generate_csv(file_name)

    print("Analiză populație...")
    analyze_population(file_name)

    print("Generare și populare hash table cu 1 milion de CNP-uri...")
    generate_csv(file_name, count=1000000)

    print("Analiză performanță căutări...")
    analyze_search_performance(count=1000)


if __name__ == "__main__":
    main()
