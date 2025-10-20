import csv

# lista de litere in ordinea aproximativa a frecventei
LETTER_FREQUENCY = list("AEIRSTULNOCMDPĂFÎÂȘȚGBHJXKQWYZ")
VOWELS = list("AEIOUĂÂÎ")
CONSONANTS = [l for l in LETTER_FREQUENCY if l not in VOWELS]
RARE_LETTERS = ["Q","W","X","Y","K","J"]  # litere rare
RARE_PENALTY = 5  # penalizare pentru litere rare

# citeste jocurile din fisier csv
def read_input_file(filename):
    games = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            if len(row) < 3:
                print("Linie sarita (format incorect):", row)
                continue
            game_id = row[0].strip()
            pattern = row[1].strip()  # pattern cu *
            target = row[2].strip()   # cuvantul tinta
            games.append((game_id, pattern, target))
    return games

# actualizeaza lista de litere posibile de ghicit
def update_possible_letters(possible_letters, pattern, guessed_letters):
    new_possible = []
    for l in possible_letters:
        if l not in guessed_letters and l not in pattern:
            new_possible.append(l)
    return new_possible

# ghiceste un cuvant
def auto_guess_word(pattern_initial, answer, letter_order):
    pattern = list(pattern_initial.upper())  # transforma pattern in lista
    answer_upper = answer.upper()
    guessed_letters = []
    for ch in pattern:
        if ch != "*":
            guessed_letters.append(ch)

    attempts = 0
    sequence = []

    possible_letters = letter_order.copy()

    while "*" in pattern:  # cat timp mai sunt litere necunoscute
        possible_letters = update_possible_letters(possible_letters, pattern, guessed_letters)
        guess = None
        for l in letter_order:  # ia litere in ordinea prioritatii
            if l in possible_letters:
                guess = l
                break
        if guess is None:
            break

        guessed_letters.append(guess)
        sequence.append(guess)
        attempts += 1

        # completeaza toate pozitiile cu litera ghicita
        for i in range(len(pattern)):
            if answer_upper[i] == guess:
                pattern[i] = guess

    word_found = "".join(pattern)
    status = "OK" if word_found == answer_upper else "EROARE"
    return attempts, word_found, status, sequence

# actualizeaza scorurile literelor ghicite
def update_letter_scores(letter_scores, word):
    for ch in word.upper():
        index = -1
        for i in range(len(letter_scores)):
            if letter_scores[i][0] == ch:
                index = i
                break
        if index != -1:
            letter_scores[index][1] += 1  # creste scorul
    return letter_scores

# reordoneaza literele dupa scor si penalizare pentru litere rare
def reorder_letters_by_scores(letter_scores):
    vowels_sorted = []
    consonants_sorted = []
    for l, score in letter_scores:
        # aplicam penalizare pentru litere rare
        if l in RARE_LETTERS:
            score -= RARE_PENALTY
        if l in VOWELS:
            vowels_sorted.append((l, score))
        else:
            consonants_sorted.append((l, score))
    # sortare descrescatoare dupa scor
    vowels_sorted.sort(key=lambda x: -x[1])
    consonants_sorted.sort(key=lambda x: -x[1])
    # extragem doar literele
    vowels_sorted = [l for l,s in vowels_sorted]
    consonants_sorted = [l for l,s in consonants_sorted]
    return vowels_sorted + consonants_sorted

def main():
    input_file = "listacuvinte.csv"
    output_file = "rezultate.csv"

    games = read_input_file(input_file)
    total_attempts = 0

    # initializare scor litere: lista de [litera, scor]
    letter_scores = []
    for l in LETTER_FREQUENCY:
        letter_scores.append([l, 1])  # start cu 1

    letter_order = reorder_letters_by_scores(letter_scores)

    with open(output_file, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out, delimiter=';')
        writer.writerow(["game_id","total_incercari","cuvant_gasit","status","secventa_incercari"])

        for game_id, pattern, target in games:
            attempts, found, status, seq = auto_guess_word(pattern, target, letter_order)
            total_attempts += attempts
            writer.writerow([game_id, attempts, found, status, " ".join(seq)])
            print(f"{game_id};{attempts};{found};{status};{' '.join(seq)}")

            if status == "OK":
                letter_scores = update_letter_scores(letter_scores, found)
                letter_order = reorder_letters_by_scores(letter_scores)

    print("\nTotal incercari pentru toate jocurile:", total_attempts)

if __name__ == "__main__":
    main()
