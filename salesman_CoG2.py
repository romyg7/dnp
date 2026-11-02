import matplotlib.pyplot as plt

# --- 1. DEFINICIJA PODATKOV IN PARAMETROV ---
# Seznam trgovin z geografskimi koordinatami in količino tovora (v tonah)
trgovine = [
    {"ime": "Ljubljana", "x": 14.5058, "y": 46.0569, "tovor": 150},
    {"ime": "Maribor",   "x": 15.6459, "y": 46.5547, "tovor": 90},
    {"ime": "Celje",     "x": 15.2674, "y": 46.2360, "tovor": 60},
    {"ime": "Koper",     "x": 13.7301, "y": 45.5481, "tovor": 110},
    {"ime": "Novo mesto","x": 15.1604, "y": 45.7981, "tovor": 40}
]

# Logistični finančni parametri za predavanje
CENA_GORIVA_LITER = 1.50   # v EUR
PORABA_TOVORNJAKA_100KM = 30.0  # litrov na 100 km
STROSEK_NA_KM = (PORABA_TOVORNJAKA_100KM / 100) * CENA_GORIVA_LITER

# --- 2. IZRACUN TEŽIŠČA (Center of Gravity) ---
skupni_tovor = sum(t["tovor"] for t in trgovine)
skladisce_x = sum(t["x"] * t["tovor"] for t in trgovine) / skupni_tovor
skladisce_y = sum(t["y"] * t["tovor"] for t in trgovine) / skupni_tovor

# Vstavimo izračunano lokacijo v seznam vseh točk
LOKACIJE = {"Izračunano skladišče": (skladisce_x, skladisce_y)}
for t in trgovine:
    LOKACIJE[t["ime"]] = (t["x"], t["y"])

# --- 3. CESTNA MATRIKA RAZDALJ (v kilometrih) ---
# Ker izračunano skladišče pade nekje v okolico Grosupljega/Ivančne Gorice,
# so spodaj vnešene realne cestne razdalje do mest in med mesti.
CESTNE_RAZDALJE = {
    "Izračunano skladišče": {"Ljubljana": 32, "Maribor": 145, "Celje": 93, "Koper": 134, "Novo mesto": 45},
    "Ljubljana": {"Izračunano skladišče": 32, "Maribor": 127, "Celje": 79, "Koper": 104, "Novo mesto": 72},
    "Maribor":   {"Izračunano skladišče": 145, "Ljubljana": 127, "Celje": 52, "Koper": 229, "Novo mesto": 158},
    "Celje":     {"Izračunano skladišče": 93, "Ljubljana": 79, "Maribor": 52, "Koper": 182, "Novo mesto": 90},
    "Koper":     {"Izračunano skladišče": 134, "Ljubljana": 104, "Maribor": 229, "Celje": 182, "Novo mesto": 174},
    "Novo mesto":{"Izračunano skladišče": 45, "Ljubljana": 72, "Maribor": 158, "Celje": 90, "Koper": 174}
}

# --- 4. ALGORITEM NAJBLIŽJEGA SOSEDA (TSP) ---
def optimizacija_dostave(razdalje, zacetek):
    neobiskane = list(razdalje[zacetek].keys())
    trenutna = zacetek
    pot = [zacetek]
    skupni_km = 0.0

    print("--- POTEK DISTRIBUCIJSKE POTI ---")
    while neobiskane:
        naslednja = min(neobiskane, key=lambda x: razdalje[trenutna][x])
        prevoženi_km = razdalje[trenutna][naslednja]
        
        skupni_km += prevoženi_km
        pot.append(naslednja)
        neobiskane.remove(naslednja)
        
        print(f"Kamion pelje: {trenutna} -> {naslednja} ({prevoženi_km} km)")
        trenutna = naslednja

    # Povratek nazaj v skladišče
    nazaj_v_bazo = razdalje[trenutna][zacetek]
    skupni_km += nazaj_v_bazo
    pot.append(zacetek)
    print(f"Povratek: {trenutna} -> {zacetek} ({nazaj_v_bazo} km)\n")
    
    return pot, skupni_km

# --- 5. ZAGON IN IZRAČUN FINANČNE METRIKE ---
zacetna_tocka = "Izračunano skladišče"
koncna_pot, končni_kilometri = optimizacija_dostave(CESTNE_RAZDALJE, zacetna_tocka)

skupni_strosek_eur = končni_kilometri * STROSEK_NA_KM
potrebno_gorivo_litri = (končni_kilometri / 100) * PORABA_TOVORNJAKA_100KM

print("--- REZULTAT LOGISTIČNE ANALIZE ---")
print(f"Optimalna lokacija skladišča (koordinate): X={skladisce_x:.4f}, Y={skladisce_y:.4f}")
print(f"Zaporedje dostave: {' -> '.join(koncna_pot)}")
print(f"Skupna pot prevoza: {končni_kilometri:.1f} km")
print(f"Porabljeno dizelsko gorivo: {potrebno_gorivo_litri:.1f} l")
print(f"Strošek goriva za celotno turo: {skupni_strosek_eur:.2f} EUR\n")

# --- 6. VIZUALIZACIJA (Matplotlib) ---
plt.figure(figsize=(10, 7))
plt.grid(True, linestyle='--', alpha=0.5)

# Izris poti s puščicami
for i in range(len(koncna_pot) - 1):
    t1, t2 = koncna_pot[i], koncna_pot[i+1]
    x1, y1 = LOKACIJE[t1]
    x2, y2 = LOKACIJE[t2]
    plt.annotate('', xy=(x2, y2), xytext=(x1, y1),
                 arrowprops=dict(arrowstyle="->", color="darkgreen", lw=2.5, ls="-"))

# Izris trgovin (velikost kroga glede na količino tovora)
for t in trgovine:
    plt.scatter(t["x"], t["y"], s=t["tovor"]*6, color='royalblue', edgecolors='black', zorder=3)
    plt.text(t["x"] + 0.04, t["y"] + 0.02, f"{t['ime']} ({t['tovor']}t)", fontsize=10, fontweight='bold')

# Izris skladišča
plt.scatter(skladisce_x, skladisce_y, s=400, color='crimson', marker='*', edgecolors='black', label='Novo skladišče', zorder=4)
plt.text(skladisce_x + 0.04, skladisce_y - 0.05, "IZHODIŠČE (Težišče)", color='crimson', fontsize=10, fontweight='bold')

plt.title("Logistična optimizacija: Cestni TSP & Stroškovna analiza", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Geografska dolžina")
plt.ylabel("Geografska širina")
plt.tight_layout()
plt.show()
