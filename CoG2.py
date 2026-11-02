import matplotlib.pyplot as plt

# Seznam trgovin z realnimi koordinatami in količino tovora v tonah
trgovine = [
    {"ime": "Ljubljana", "x": 14.5058, "y": 46.0569, "tovor": 150},
    {"ime": "Maribor",   "x": 15.6459, "y": 46.5547, "tovor": 90},
    {"ime": "Celje",     "x": 15.2674, "y": 46.2360, "tovor": 60},
    {"ime": "Koper",     "x": 13.7301, "y": 45.5481, "tovor": 110},
    {"ime": "Novo mesto","x": 15.1604, "y": 45.7981, "tovor": 40}
]

# 1. Izračun težišča (Center of Gravity)
skupni_tovor = sum(t["tovor"] for t in trgovine)
idealni_x = sum(t["x"] * t["tovor"] for t in trgovine) / skupni_tovor
idealni_y = sum(t["y"] * t["tovor"] for t in trgovine) / skupni_tovor

# 2. Nastavitev grafikona
plt.figure(figsize=(10, 7))
plt.grid(True, linestyle='--', alpha=0.5)

# 3. Izris oskrbovalnih poti (povezave med skladiščem in trgovinami)
for t in trgovine:
    plt.plot([idealni_x, t["x"]], [idealni_y, t["y"]], color='gray', linestyle=':', alpha=0.7, zorder=1)

# 4. Izris trgovin (velikost točke je odvisna od količine tovora)
for t in trgovine:
    velikost = t["tovor"] * 5  # Skaliranje za boljšo vidnost
    plt.scatter(t["x"], t["y"], s=velikost, color='royalblue', edgecolors='black', alpha=0.8, zorder=2)
    plt.text(t["x"] + 0.05, t["y"] + 0.02, f"{t['ime']} ({t['tovor']}t)", fontsize=10, fontweight='bold')

# 5. Izris optimalne lokacije skladišča
plt.scatter(idealni_x, idealni_y, s=350, color='crimson', marker='*', edgecolors='black', label='Optimalno skladišče', zorder=3)
plt.text(idealni_x + 0.05, idealni_y - 0.05, "CENTRALNO SKLADIŠČE", color='crimson', fontsize=10, fontweight='bold')

# 6. Napisi in oblikovanje
plt.title("Logistična mreža: Gravitacijski center in oskrbovalne poti", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Geografska dolžina (X)", fontsize=11)
plt.ylabel("Geografska širina (Y)", fontsize=11)
plt.legend(loc="upper left")

# Prikaz grafikona na zaslonu
plt.tight_layout()
plt.show()
