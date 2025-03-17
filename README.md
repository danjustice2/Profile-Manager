# DynamicTemplate Profile Manager

Dette værktøj gør det nemt at dele lokale profiler mellem kolleger i DynamicTemplate-miljøet ved brug af det fælles Q-drev.

## Hvorfor dette værktøj?

I DynamicTemplate bliver afsenderoplysninger typisk hentet fra brugerens Active Directory-profil. Alternativt kan man bruge \"lokale profiler\", der gemmes lokalt på hver brugers enhed som XML-filer. Det er imidlertid ikke muligt med DynamicTemplates standardfunktionalitet at dele disse lokale profiler mellem kolleger.

Dette værktøj løser netop den udfordring, så brugere let kan:

- Dele profiler med andre via et fælles Q-drev.
- Importere profiler delt af kolleger hurtigt og enkelt.

## Brugsscenarier

- **Breve fra afdelingen som helhed:**  
  Nogle afdelinger kan have behov for at sende breve fra afdelingen i stedet for fra en enkelt medarbejder.

## Installation og brug

### Forudsætninger
- Skriveadgang til følgende sti på Q-drev, som delte profiler bliver lagt i:
  ```
  Q:\\DynamicTemplate\\Delte Profiler
  ```
- Skrive adgang til følgende sti, som lokale profiler ligger i:
  ```
  %APPDATA%\\dynamictemplate\\Profiler
  ```

**Bemærk:** Ovenstående stier kan tilpasses ved redigering af filen `config/config.json`.

### Fremgangsmåde

1. **Eksportér (del) en profil:**
   - Når man vælger at dele en profil, vises en liste over tilgængelige profiler på ens lokale maskine.
   - Profilen kopieres derefter til Q-drevet under en mappe med ens brugernavn.

2. **Importér en delt profil:**
   - Indtast kollegaens brugernavn ved import.
   - Værktøjet søger i:
     ```
     Q:\\DynamicTemplate\\Delte Profiler\\[kollegas brugernavn]\\
     ```
   og importerer den ønskede profil til lokale profiler.

## Teknisk baggrund

Værktøjet er udviklet i Python, og den primære fil er `main.py`. For at gøre brugen let og brugervenlig findes en kompileret `.exe`-fil lavet med PyInstaller. Dette betyder, at slutbrugere ikke nødvendigvis skal have Python installeret for at køre programmet.

### Avancerede indstillinger
- Profilerne ligger som XML-filer på lokal enhed.
- Stier og andre indstillinger kan ændres i `config/config.json`.
- Vær opmærksom på, at ændring af config.json kræver ny kompilering via PyInstaller, hvis man benytter den kompilerede EXE-version.

## Udviklingsopsætning

### Krav:
- Python 3.x 
- (optional) PyInstaller (`pip install pyinstaller`)

### Kørsel direkte fra Python:

```bash
git clone [repository-link-here]
cd [repository-map-here]
python main.py
```

### Kompilering med PyInstaller (til distribution):

```bash
pyinstaller --onefile --add-data \"config/config.json;config\" main.py
```

**OBS:** Efter kompilering vil `config.json`-indstillingerne være bundet til `.exe`-filen.

## Support

Har du problemer, spørgsmål eller forslag til forbedringer? Kontakt [darju@toender.dk](mailto:darju@toender.dk).

## Licens

MIT License

Copyright (c) 2025 Danny Ray Justice

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.