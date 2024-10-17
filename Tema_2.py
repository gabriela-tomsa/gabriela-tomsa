text="""  Pe primele nouă luni din 2024, înmatriculările de autoturisme second hand înmatriculate pentru prima oară în România au ajuns la valoarea de 239.066 unități, în scădere cu -1.21% faţă de perioada similară din 2023. respectiv 241.992 unității"""
jumatate=len(text)//2
prima_jumatate=text[:jumatate]
a_doua_jumatate=text[jumatate:]
prima_jumatate=prima_jumatate.upper()
prima_jumatate=prima_jumatate.strip(" ")

a_doua_jumatate=a_doua_jumatate[::-1]
a_doua_jumatate=a_doua_jumatate.capitalize()
a_doua_jumatate=a_doua_jumatate.replace(".", "")
a_doua_jumatate=a_doua_jumatate.replace(",", "")
a_doua_jumatate=a_doua_jumatate.replace("!", "")
a_doua_jumatate=a_doua_jumatate.replace("?", "")

text=prima_jumatate+a_doua_jumatate

print(text)