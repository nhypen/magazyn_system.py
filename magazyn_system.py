import os
import json

DANE_FILE = "dane.txt"
HISTORIA_FILE = "historia.txt"

if os.path.exists(DANE_FILE):
    with open(DANE_FILE, "r") as f:
        dane = json.load(f)
        saldo = dane.get("saldo", 0)
        magazyn = dane.get("magazyn", {})

if os.path.exists(HISTORIA_FILE):
    with open(HISTORIA_FILE, "r") as f:
        historia = [linia.strip() for linia in f.readlines()]

saldo = 0
magazyn = {}
historia = []
komendy = ["saldo", "sprzedaż", "zakup", "konto", "lista", "magazyn", "przegląd", "koniec"]

# BONUS! Tytuł programu
print("=======================================")
print("  SYSTEM KSIĘGGOWO-MAGAZYNOWY     ")
print("======================================")

while True:
    print("\nDostępne komendy:")
    for k in komendy:
        print("-", k)

    komenda = input("\nWpisz komendę: ").lower()

    if komenda == "koniec":
        print("Kończę działanie programu.")
        with open("historia.txt", "w") as plik:
            for i, operacja in enumerate(historia):
                plik.write(f"{i}. {operacja}\n")
        print("Historia operacji została zapisana do pliku 'historia.txt'")
        break

        with open("historia.txt", "a") as plik:
            for operacja in historia:
                plik.write(f"{operacja}\n")
        print("Historia operacji została dopisana do pliku 'historia.txt'.")

        with open("dane.txt", "w") as f:
            import json
            json.dump({
                "saldo": saldo,
                "magazyn": magazyn

            }, f)
        print("Stan salda i magazynu został zapisany do pliku 'dane.txt'.")

        break

    elif komenda not in komendy:
        print("Nieznana komenda. Sprubój ponownie.")
        continue

    elif komenda == "konto":
        print(f"Stan konta: {saldo} zł")

    elif komenda == "lista":
        print("Stan magazynu:")
        for produkt, (cena, ilosc) in magazyn.items():
            print(f"- {produkt}: {ilosc} szt. (cena: {cena} zł)")

    elif komenda == "saldo":
        try:
            kwota = int(input("Podaj kwotę (dodatnia lub ujemna): "))
            opis = input("Podaj opis operacji: ")

            if saldo + kwota < 0:
                print("Błąd: saldo nie może być ujemne!")
            else:
                saldo += kwota
                historia.append(("saldo", kwota, opis))
                print(f"Operacja zakończona. Nowe saldo: {saldo} zł")

        except ValueError:
            print("Błąd: kwota musi być liczbąc całkowitą!")

    elif komenda == "zakup":
        try:
            nazwa = input("Podaj nazwę produktu: ")
            cena = int(input("Podaj cenę jednostkową: "))
            ilosc = int(input("Podaj ilość sztuk: "))
            koszt = cena * ilosc

            if cena < 0 or ilosc <= 0:
                print("Cena i ilość muszą byc dodatnie!")
            elif saldo < koszt:
                print("Błąd: za mało środków na koncie!")
            else:
                saldo -= koszt
                if nazwa in magazyn:
                    magazyn[nazwa][1] += ilosc
                else:
                    magazyn[nazwa] = [cena, ilosc]
                historia.append(("zakup", nazwa, cena, ilosc))
                print(f"Zakup zakończony. Pozostałe saldo: {saldo} zł")

        except ValueError:
            print("Błąd: cena i ilość muszą być liczbami całkowitymi!")

    elif komenda == "sprzedaż":
        try:
            nazwa = input("Podaj nazwę produktu: ")
            cena = int(input("Podaj cenę sporzedaży za sztukę: "))
            ilosc = int(input("Podaj ilość sztuk do sprzedaży: "))

            if nazwa not in magazyn:
                print("Produkt nie istnieje w magazynie!")
            elif ilosc <= 0 or cena <= 0:
                print("Cena i ilość muszą być dodatnie!")
            elif magazyn[nazwa][1] < ilosc:
                print("Za mało sztuk w magazynie!")
            else:
                magazyn[nazwa][1] -= ilosc
                saldo += cena * ilosc
                historia.append(("sprzedaż", nazwa, cena, ilosc))
                print(f"Sprzedaż zakończona. Nowe saldo: {saldo} zł")
                if magazyn[nazwa][1] == 0:
                    del magazyn[nazwa]

        except ValueError:
            print("Błąd: cena i ilość muszą być liczbami całkowitymi!")

    elif komenda == "magazyn":
        nazwa = input("Podaj nazwę produktu, który chcesz sprawdzić: ")
        if nazwa in magazyn:
            cena, ilosc = magazyn[nazwa]
            print(f"{nazwa} - {ilosc} szt. (cena {cena} zł)")
        else:
            print("Taki produkt nie znajduje się w magazynie.")

    elif komenda == "przegląd":
        try:
            od = input("Od którego indeksu (ENTER = początek): ")
            do = input("Do którego indeksu (ENTER = koniec): ")

            start = int(od.strip()) if od.strip() != "" else 0
            end = int(do.strip()) if do.strip() != "" else len(historia)

            if start < 0 or end > len(historia) or start > end:
                print(f"Błąd: Zakres poza historią operacji!")
            else:
                print(f"Przegląd operacji od {start} do {end -1 }:")
                for i, operacja in enumerate(historia[start:end], start):
                    print(f"{i}. {operacja}")

        except ValueError:
            print("Błąd: Podane wartości muszą byc liczbami lub puste.")

