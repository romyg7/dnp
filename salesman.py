import math

# 1. DEFINICIJA PODATKOV: Lokacije skladišč/strank (X, Y koordinate v kilometrih)
# Predstavlja lokacije, ki jih mora dostavno vozilo obiskati.
LOKACIJE = {
    "Skladišče (Zacetek)": (0, 0),
    "Maribor": (40, 50),
    "Celje": (20, 25),
    "Ljubljana": (-40, -10),
    "Koper": (-90, -50),
    "Novo mesto": (0, -30)
}

def izracunaj_razdaljo(tocka1, tocka2):
    """Izračuna zračno (Evklidsko) razdaljo med dvema točkama."""
    return math.sqrt((tocka1[0] - tocka2[0])**2 + (tocka1[1] - tocka2[1])**2)

def nacrtuj_pot_najblizji_sosed(lokacije, zacetna_tocka):
    """
    Hevristični algoritem 'Najbližji sosed' za logistično optimizacijo poti.
    Vozilo vedno izbere najbližjo naslednjo neobiskano lokacijo.
    """
    neobiskane = list(lokacije.keys())
    neobiskane.remove(zacetna_tocka)
    
    trenutna_tocka = zacetna_tocka
    pot = [zacetna_tocka]
    skupna_razdalja = 0.0

    print(print("--- ZACETEK NACRTOVANJA POTI ---"))
    
    while neobiskane:
        najblizja_tocka = None
        najkrajsa_razdalja = float('inf') # Nastavimo na neskončno za primerjavo

        # Poišči najbližjo neobiskano lokacijo
        for naslednja_tocka in neobiskane:
            razdalja = izracunaj_razdaljo(lokacije[trenutna_tocka], lokacije[naslednja_tocka])
            if razdalja < najkrajsa_razdalja:
                najkrajsa_razdalja = razdalja
                najblizja_tocka = naslednja_tocka

        # Posodobi stanje (premik na novo lokacijo)
        skupna_razdalja += najkrajsa_razdalja
        pot.append(najblizja_tocka)
        neobiskane.remove(najblizja_tocka)
        
        print(f"Premik: {trenutna_tocka} -> {najblizja_tocka} ({najkrajsa_razdalja:.2f} km)")
        trenutna_tocka = najblizja_tocka

    # Na koncu se vozilo vrne nazaj v začetno skladišče
    razdalja_za_nazaj = izracunaj_razdaljo(lokacije[trenutna_tocka], lokacije[zacetna_tocka])
    skupna_razdalja += razdalja_za_nazaj
    pot.append(zacetna_tocka)
    print(f"Povratek: {trenutna_tocka} -> {zacetna_tocka} ({razdalja_za_nazaj:.2f} km)")

    return pot, skupna_razdalja

# --- ZAGON PROGRAMA ---
zacetek = "Skladišče (Zacetek)"
koncna_pot, končna_razdalja = nacrtuj_pot_najblizji_sosed(LOKACIJE, zacetek)

print("\n--- REZULTAT OPTIMIZACIJE ---")
print("Predlagana pot dostave:")
print(" -> ".join(koncna_pot))
print(f"Skupna dolžina poti: {končna_razdalja:.2f} km")
