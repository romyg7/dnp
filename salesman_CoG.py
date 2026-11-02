import math
import matplotlib.pyplot as plt

# 1. DEFINICIJA PODATKOV: Trgovine z realnimi geografskimi koordinatami in tovorom
trgovine = [
    {"ime": "Ljubljana", "x": 14.5058, "y": 46.0569, "tovor": 150},
    {"ime": "Maribor",   "x": 15.6459, "y": 46.5547, "tovor": 90},
    {"ime": "Celje",     "x": 15.2674, "y": 46.2360, "tovor": 60},
    {"ime": "Koper",     "x": 13.7301, "y": 45.5481, "tovor": 110},
    {"ime": "Novo mesto","x": 15.1604, "y": 45.7981, "tovor": 40}
]

# 2. IZRACUN TEŽIŠČA (Center of Gravity)
skupni_tovor = sum(t["tovor"] for t in trgovine)
skladisce_x = sum(t["x"] * t["tovor"] for t in trgovine) / skupni_tovor
skladisce_y = sum(t["y"] * t["tovor"] for t in trgovine) / skupni_tovor

# Ustvarimo koordinatni slovar za TSP
LOKACIJE = {"Izračunano skladišče": (skladisce_x, skladisce_y)}
for t in trgovine:
    LOKACIJE[t["ime"]] = (t["x"], t["y"])


# 3. POPRAVLJEN IZRACUN RAZDALJE V KILOMETRIH
def izracunaj_razdaljo_km(tocka1, tocka2):
    """
    Izračuna približno zračno razdaljo v kilometrih med dvema geografskima točkama.
    Upošteva pretvorbo stopinj v kilometre za območje Slovenije.
    """
    dx = (tocka1[0] - tocka2[0]) * 77.0   # 1° geografske dolžine v SLO je cca 77 km
    dy = (tocka1[1] - tocka2[1]) * 111.0  # 1° geografske širine je cca 111 km
    return math.sqrt(dx**2 + dy**2)


# 4. ALGORITEM TRGOVSKEGA POTNIKA (Najbližji sosed)
def nacrtuj_pot_najblizji_sosed(lokacije, zacetna_tocka):
    neobiskane = list(lokacije.keys())
    neobiskane.remove(zacetna_tocka)
    
    trenutna_tocka = zacetna_tocka
    pot = [zacetna_tocka]
    skupna_razdalja = 0.0

    print("--- POTEK OPTIMIZACIJE POTI ---")
    while neobiskane:
        najblizja_tocka = None
        najkrajsa_razdalja = float('inf')

        for naslednja_tocka in neobiskane:
            # Tukaj pokličemo popravljeno funkcijo za kilometre
            razdalja = izracunaj_razdaljo_km(lokacije[trenutna_tocka], lokacije[naslednja_tocka])
            if razdalja < najkrajsa_razdalja:
                najkrajsa_razdalja = razdalja
                najblizja_tocka = naslednja_tocka

        skupna_razdalja += najkrajsa_razdalja
        pot.append(najblizja_tocka)
        neobiskane.remove(najblizja_tocka)
        
        print(f"Premik: {trenutna_tocka} -> {najblizja_tocka} ({najkrajsa_razdalja:.2f} km)")
        trenutna_tocka = najblizja_tocka

    # Povratek v izračunano skladišče
    razdalja_za_nazaj = izracunaj_razdaljo_km(lokacije[trenutna_tocka], lokacije[zacetna_tocka])
    skupna_razdalja += razdalja_za_nazaj
    pot.append(zacetna_tocka)
    print(f"Povratek: {trenutna_tocka} -> {zacetna_tocka} ({razdalja_za_nazaj:.2f} km)\n")

    return pot, skupna_razdalja


# --- ZAGON OPTIMIZACIJE ---
zacetna_tocka = "Izračunano skladišče"
koncna_pot, končna_razdalja = nacrtuj_pot_najblizji_sosed(LOKACIJE, zacetna_tocka)

print("--- KONČNI REZULTAT ---")
print(f"Izračunano težišče skladišča: X={skladisce_x:.4f}, Y={skladisce_y:.4f}")
print("Zaporedje obiska lokacij:")
print(" -> ".join(koncna_pot))
print(f"Skupna dolžina logistične poti: {končna_razdalja:.2f} km\n")


# 5. VIZUALIZACIJA
plt.figure(figsize=(10, 7))
plt.grid(True, linestyle='--', alpha=0.5)

# Izris poti vozila (puščice)
for i in range(len(koncna_pot) - 1):
    t1 = koncna_pot[i]
    t2 = koncna_pot[i+1]
    x1, y1 = LOKACIJE[t1]
    x2, y2 = LOKACIJE[t2]
    plt.annotate('', xy=(x2, y2), xytext=(x1, y1),
                 arrowprops=dict(arrowstyle="->", color="darkgreen", lw=2, ls="-"))

# Izris trgovin
for t in trgovine:
    plt.scatter(t["x"], t["y"], s=t["tovor"]*5, color='royalblue', edgecolors='black', zorder=3)
    plt.text(t["x"] + 0.03, t["y"] + 0.02, f"{t['ime']} ({t['tovor']}t)", fontsize=10, fontweight='bold')

# Izris skladišča
plt.scatter(skladisce_x, skladisce_y, s=350, color='crimson', marker='*', edgecolors='black', label='Novo skladišče', zorder=4)
plt.text(skladisce_x + 0.03, skladisce_y - 0.05, "IZHODIŠČE", color='crimson', fontsize=10, fontweight='bold')

plt.title("Optimizacija poti v kilometrih (TSP - Najbližji sosed)", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Geografska dolžina (stopinje)")
plt.ylabel("Geografska širina (stopinje)")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()