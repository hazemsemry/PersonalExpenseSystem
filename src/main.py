import sqlite3

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# aggiunge una nuova categoria
def aggiungi_categoria():
    nome = input("Nome categoria: ")

    if nome == "":
        print("Nome non valido")
        return

    cursor.execute("SELECT * FROM categories WHERE name = ?", (nome,))
    if cursor.fetchone():
        print("Categoria già esistente")
    else:
        cursor.execute("INSERT INTO categories(name) VALUES (?)", (nome,))
        conn.commit()
        print("Categoria aggiunta")

# inserisce una spesa
def inserisci_spesa():
    data = input("Data (YYYY-MM-DD): ")

    try:
        importo = float(input("Importo: "))
        if importo <= 0:
            print("Importo non valido")
            return
    except:
        print("Devi inserire un numero")
        return

    categoria = input("Categoria: ")
    desc = input("Descrizione: ")

    cursor.execute("SELECT id FROM categories WHERE name = ?", (categoria,))
    result = cursor.fetchone()

    if not result:
        print("Categoria non trovata")
        return

    cat_id = result[0]

    cursor.execute("""
        INSERT INTO expenses(date, amount, category_id, description)
        VALUES (?, ?, ?, ?)
    """, (data, importo, cat_id, desc))

    conn.commit()
    print("Spesa salvata")

# imposta il budget
def definisci_budget():
    mese = input("Mese (YYYY-MM): ")
    categoria = input("Categoria: ")

    try:
        budget = float(input("Budget: "))
        if budget <= 0:
            print("Valore non valido")
            return
    except:
        print("Devi inserire un numero")
        return

    cursor.execute("SELECT id FROM categories WHERE name = ?", (categoria,))
    result = cursor.fetchone()

    if not result:
        print("Categoria non trovata")
        return

    cat_id = result[0]

    try:
        cursor.execute("""
            INSERT INTO budgets(month, category_id, amount)
            VALUES (?, ?, ?)
        """, (mese, cat_id, budget))
    except:
        cursor.execute("""
            UPDATE budgets
            SET amount = ?
            WHERE month = ? AND category_id = ?
        """, (budget, mese, cat_id))

    conn.commit()
    print("Budget salvato")

# report totale per categoria
def report_totale():
    cursor.execute("""
        SELECT c.name, SUM(e.amount)
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        GROUP BY c.name
    """)

    dati = cursor.fetchall()

    print("\nTotale per categoria:")
    for r in dati:
        print(r[0], "-", r[1])

# confronto budget
def report_budget():
    cursor.execute("""
        SELECT b.month, c.name, b.amount,
               IFNULL(SUM(e.amount), 0)
        FROM budgets b
        JOIN categories c ON b.category_id = c.id
        LEFT JOIN expenses e ON e.category_id = c.id
        GROUP BY b.month, c.name
    """)

    dati = cursor.fetchall()

    for r in dati:
        mese, cat, budget, speso = r

        if speso > budget:
            stato = "SUPERATO"
        else:
            stato = "OK"

        print("\nMese:", mese)
        print("Categoria:", cat)
        print("Budget:", budget)
        print("Speso:", speso)
        print("Stato:", stato)

# lista spese
def lista_spese():
    cursor.execute("""
        SELECT e.date, c.name, e.amount, e.description
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        ORDER BY e.date
    """)

    dati = cursor.fetchall()

    print("\nData - Categoria - Importo - Descrizione")
    for r in dati:
        print(f"{r[0]} - {r[1]} - {r[2]} - {r[3]}")

# menu report
def menu_report():
    while True:
        print("\n--- REPORT ---")
        print("1. Totale per categoria")
        print("2. Spese vs budget")
        print("3. Lista spese")
        print("4. Indietro")

        scelta = input("Scelta: ")

        if scelta == "1":
            report_totale()
        elif scelta == "2":
            report_budget()
        elif scelta == "3":
            lista_spese()
        elif scelta == "4":
            break
        else:
            print("Scelta non valida")

# menu principale
def menu():
    print("\n--- SPESE PERSONALI ---")
    print("1. Categorie")
    print("2. Inserisci spesa")
    print("3. Budget")
    print("4. Report")
    print("5. Esci")

while True:
    menu()
    scelta = input("Scelta: ")

    if scelta == "1":
        aggiungi_categoria()
    elif scelta == "2":
        inserisci_spesa()
    elif scelta == "3":
        definisci_budget()
    elif scelta == "4":
        menu_report()
    elif scelta == "5":
        print("Chiusura programma")
        break
    else:
        print("Scelta non valida")

conn.close()