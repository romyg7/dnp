# Seznam strank/trgovin z njihovimi X, Y koordinatami in količino tovora (v tonah)
trgovine = [
    {"ime": "Ljubljana", "x": 46.05, "y": 14.50, "tovor": 150},
    {"ime": "Maribor",   "x": 46.55, "y": 15.64, "tovor": 500},
    {"ime": "Celje",     "x": 46.23, "y": 15.26, "tovor": 60},
    {"ime": "Koper",     "x": 45.54, "y": 13.73, "tovor": 110},
    {"ime": "Novo mesto","x": 45.80, "y": 15.17, "tovor": 40}
]

# Inicializacija spremenljivk za izračun težišča
skupni_tovor = 0
utežena_vsota_x = 0
utežena_vsota_y = 0

print("--- ANALIZA LOGISTIČNE MREŽE ---")

# Sprehod skozi vse lokacije in izračun potrebnih podatkov
for t in trgovine:
    print(f"Trgovina {t['ime']}: lokacija ({t['x']}, {t['y']}), količina = {t['tovor']} t")
    
    skupni_tovor += t["tovor"]
    utežena_vsota_x += t["x"] * t["tovor"]
    utežena_vsota_y += t["y"] * t["tovor"]

# Izračun idealnih koordinat za centralno skladišče (težišče)
idealni_x = round(utežena_vsota_x / skupni_tovor, 2)
idealni_y = round(utežena_vsota_y / skupni_tovor, 2)

print("\n--- REZULTAT OPTIMIZACIJE ---")
print(f"Skupna količina oskrbovanega tovora: {skupni_tovor} ton")
print(f"Optimalna lokacija za novo centralno skladišče je na koordinatah:")
print(f"X (Geografska širina): {idealni_x}")
print(f"Y (Geografska dolžina): {idealni_y}")
