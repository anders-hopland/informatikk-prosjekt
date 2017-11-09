# informatikk-prosjekt

Informatikk prosjektarbeid er et fag på NTNU som har som formål å være et større IT prosjekt hvor studentene får erfaring fra å jobbe i team og å lage et større prosjekt fra bunnen av. Gjennom prosjektet får elevene erfaring med scrum, git, og eventuelt nye teknologier.

# Hvordan sette opp utviklingsmiljø
For å sette opp utviklingsmiljø starter en med å clone git repoet
- Om du bruker ssh cloner du repoet ved å kopiere følgene inn i terminalen `git@github.com:anders-hopland/informatikk-prosjekt.git`
- Om du bruker https cloner du repoet ved å kopiere følgene inn i terminalen `https://github.com/anders-hopland/informatikk-prosjekt.git`

For å sjekke at du har prosjektet kan du skrive `ls` i terminalen, og vil da se at det vil være en mappe `informatikk-prosjektarbeid` der

For kunne kjøre prosjektet lokalt på pcen trenger du python og django. I dette prosjektet bruker vi python 3. 
Om du lurer på om du har python 3 på maskiner skriver du `python3 --version` og vil da se om du har python, og isåfall hvilken versjon du har. Om du ikke har python 3 kan du laste det ned på følgende måte:
-  Om du er på en windows datamaskin får du tak python 3 ved å gå inn på følgende side og laste ned https://www.python.org/downloads/
-  Om du er på en maskin som kjører OSX kan du enten laste ned fra https://www.python.org/downloads/ eller laste ned via homebrew om du har dette installert på maskinen. Dette gjør du ved å skrive `brew install python3` i terminalen din, så ordner homebrew resten
-  Om du er på en maskin som kjører linux skriver du `apt-get install python3` i terminalen din, så ordner apt resten for deg

Etter at du har lastet ned python 3 må du laste ned django. Dette gjøres ved å skrive `pip3 install django` i terminalen. Pass på at du har django versjon 1.11 eller senere.

For å kjøre serveren og se at alt funker skriver du: 
-   `cd informatikk-prosjektarbeid/mysite`
-   `python3 manage.py makemigrations`
-   `python3 manage.py runserver`
- Deretter åpner du nettleseren din og går inn på `http://127.0.0.1:8000/`. Om du nå får opp noe vet du at alt funker.

Om du har make (unix kommando) kan du skrive:
-   `cd informatikk-prosjektarbeid/mysite`
-   `make build`
-   `make runserver`

For å hente inn eksempeldata må du ha make. Du kan du skrive:
-    `make rebuild-db`

Denne kommandoen henter inn eksempeldata fra users.json og skriver inn til databasen. Om kommandoen ikke fungerer, sjekk at du har filen users.json. Ved problemer, kontakt Anders Mølster Hopland.

Om du lurer på noe angående hvordan prosjektet er satt opp, sjekk ut prosjektets wiki sider, der ligger det mye oppdatert informasjon. 
