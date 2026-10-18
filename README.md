# Tartu ringmajanduse kaart

Interaktiivne kaart Tartu ringmajanduspunktidest (Leaflet + OpenStreetMap), ilma ehitusetapita: lihtsalt kolm faili.

- `index.html` on leht ise (filtrid, otsing, "lähimad mulle", popup iga punkti infoga)
- `data.js` on kõik punktid (nimi, aadress, koordinaadid, lahtiolek, mida võetakse vastu, allikas)
- `geocode.py` on valikuline, kirjutab puuduvad koordinaadid püsivalt `data.js` faili

## GitHubi lehena üles panemine (GitHub Pages)

1. Tee GitHubis uus repo (nt `tartu-ringmajandus-kaart`), avalik.
2. Lae sinna üles `index.html`, `data.js`, `geocode.py` ja `README.md` (Add file → Upload files).
3. Repo **Settings → Pages → Build and deployment**: Source = *Deploy from a branch*, Branch = `main`, kaust `/ (root)`, Save.
4. Minuti pärast on leht aadressil `https://KASUTAJANIMI.github.io/tartu-ringmajandus-kaart/`.

## Andmete kvaliteet

- 24 punkti koordinaadid pärinevad allikatest (Google Mapsi viited Humana ja Sõbralt Sõbrale lehtedelt, Kraamikaardi lehed).
- 5 punkti (Selli jäätmejaam, Uuskasutuskeskus Kalda tee, ringkasutuspank, Tehnikaringlus, paranduskelder) ja planeeritud Mõisavahe jaam on esialgu ilma koordinaatideta. Leht otsib need brauseris aadressi järgi OpenStreetMapist ja märgib "aadressi järgi". Kui tahad need püsivalt fikseerida, jooksuta oma arvutis `python3 geocode.py`, vaata tulemus üle ja pane uuendatud `data.js` GitHubi.
- Lahtiolekuajad muutuvad, enne minekut tasub kontrollida punkti koduleheküljelt.

## Punkti lisamine

Lisa `data.js` massiivi uus objekt samade väljadega. `cat` on üks: `jaatmejaam`, `taaskasutus`, `riided`, `elektroonika`, `ehitus`, `parandus`, `planeeritud`. Kui koordinaate pole, pane `lat` ja `lng` väärtuseks `null`.
