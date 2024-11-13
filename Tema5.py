numar_iteratii = 0
def cautare_binara(arr, start, stop, val):
    global numar_iteratii
    left = start
    right = stop
    while left <= right:
        mid = (left + right) // 2
        numar_iteratii += 1
        if arr[mid] == val:
            return mid
        elif arr[mid] < val:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def cauta_pacient(pacienti, id_pacient):
    global numar_iteratii
    numar_iteratii = 0
    n = len(pacienti)
    if pacienti[0] == id_pacient:
        print(f"Dosarul pacientului cu numărul de identificare {id_pacient} a fost găsit la poziția {0} după {numar_iteratii} pași de căutare.")
        return
    i = 1
    while i < n and pacienti[i] < id_pacient:
        numar_iteratii += 1
        i *= 2
    gasit = cautare_binara(pacienti, i // 2, min(i, n - 1), id_pacient)

    if gasit == -1:
        print(f"Dosarul pacientului cu numărul de identificare {id_pacient} nu a fost găsit. Total pași efectuați: {numar_iteratii}.")
    else:
        print(f"Dosarul pacientului cu numărul de identificare {id_pacient} a fost găsit la poziția {gasit} după {numar_iteratii} pași de căutare.")