**Naam applicatie:** SuperTrivia!

**Naam studenten:** Lars Bremmers &amp; Eric Louwers

# Samenvatting

Dit project staat in het teken van het maken van een leuk en leerzaam triviaspel op het internet. Men kan een profiel aanmaken op de site en het spel spelen. Men krijgt tien vragen, en moet deze zo goed mogelijk beantwoorden. Hieraan wordt een score toegekend waaraan gebruikers zich met elkaar kunnen meten, wat terug te zien is in de leaderboards. De ontwikkelaars voor deze website zijn Lars Bremmers en Eric Louwers.

# Features

In ons triviaspel komen de volgende features aan bod.

- Gebruikers kunnen leaderboards zien en zich meten aan elkaar.
- Gebruikers kunnen een moeilijkheidsgraad instellen, waarna zij het spel kunnen spelen op die moeilijkheidsgraad.
- Bij het spelen van het spel krijgen spelers een bepaalde score per goed beantwoorde vraag. Deze score wordt opgeslagen en kan worden vergeleken.
- Gebruikers kunnen na het spelen de antwoorden inkijken en kennis opdoen.
- Gebruikers hebben de mogelijkheid om te registreren, in te loggen, hun wachtwoord te veranderen, account te verwijderen etc.

# Minimum Viable product

De minimumeisen van het project zijn als volgt.

**Gebruikers moeten een profiel kunnen aanmaken**

Gebruikers moeten de mogelijkheid hebben om een profiel aan te maken en in te kunnen loggen. Dit hebben we in ons project verwerkt.

**Er wordt een score toegekend**

Als een gebruiker een Triviaspel speelt, dienen ze een score toegekend te krijgen. Ook dit hebben we in ons project verwerkt met de leaderboards.

**Vragen komen uit een online database**

Wij hebben een goede database gevonden waaruit we vragen kunnen halen voor het spel. Deze vragen hebben verschillende moeilijkheidsgraden. Ook dit is in ons project verwerkt.

# Afhankelijkheden

Met het maken van de website zijn we afhankelijk van diverse aspecten. Deze aspecten zijn de volgende.

**Databronnen**

Open Trivai database

Url: [https://opentdb.com/](https://opentdb.com/)

Verstrekt, volgens hun website, meer dan 3000 vragen. Deze vragen hebben verschillende moeilijkheidswaardes. Zo zouden wij waardes aan onze moeilijkheidsgraden kunnen toevoegen, waarbij Easy (0-300), Medium (300-700) en Hard (700-1000).

# Externe componenten

**Bootstrap**

[https://getbootstrap.com](https://getbootstrap.com)

Bootstrap is aantrekkelijk om te gebruiken, aangezien het een groot deel van de last van een website te programmeren van de schouders haalt. Op de site zelf worden 3 zogeheten &amp;quot;themes&amp;quot;, oftewel templates aangeboden. Deze kosten echter $99 per stuk. Dat lijkt ons iets te duur. Gelukkig worden er op allerlei andere websites wel gratis templates aangeboden.

# Vergelijkbare websites

**Trivia.fyi**

Een site waarbij je meteen triviavragen krijgt in combinatie met plaatjes. Er is echter geen optie om de vragen te beantwoorden, je kan de antwoorden enkel opvragen. Men kan hierbij geen profiel aanmaken en er zit dus ook geen online spelelement in.

**Sporcle.com**

Een grote website waarbij je verschillende trivia-spellen kunt spelen. Je kan een account aanmaken en quizzen spelen. Iedere gebruiker kan een quiz maken en die indelen op zijn of haar eigen manier. Dit kan variëren tot multiple choice, open vragen, visuele vragen en nog veel meer. Leaderboards worden bijgehouden, de site heeft een eigen community waarin men kan discussiëren, men kan badges winnen en vrienden toevoegen en uitdagen tot een bepaalde quiz. [Sporcle.com](http://Sporcle.com) is een zeer complete trivia spelsite.

**Triviaplaza.com**

Op de homepage van [triviaplaza.com](http://triviaplaza.com) dien je een categorie uit te kiezen. Eenmaal gekozen kan men een quiz selecteren en die gaan spelen. Het zijn simpele multiple choice vragen, 10 stuks per quiz. Men kan hierop geen profiel aanmaken, ze kunnen simpelweg hun score testen tegen de gemiddelde score.

# Moeilijkste delen

**Implementeren van de API**

Het implementeren van de API lijkt ons vrij lastig. Niet zozeer het toevoegen van aan de websites, maar meer de aanpassingen die er bij komen kijken. Hiermee bedoelen wij de gradaties van de moeilijkheid, de verschillende vragen die wij wel of niet willen toevoegen et cetera.

**Leaderboards**

Het toevoegen van leaderboards is een mooi idee, maar niet het makkelijkste idee. Hierbij zouden alle scores moeten worden opgeslagen in de database en daaronder worden gefilterd op de beste scores. Deze scores zouden dan in een lijst worden weergeven, gesorteerd op van hoog naar laag. Daarnaast zouden wij ook nog een leaderboard voor vrienden willen toevoegen, dus als het ware dat er twee leaderboards zijn. Hierbij kan de gebruiker zien wie van zijn vrienden de beste onderling is.

# Navigatie

De file application.py is het bestand waarin er door de website wordt genavigeerd. De routes worden hier beschreven, met de koppeling naar de html-bestanden (view). Helpers.py bevat alle functies die te maken hebben met de site zelf. Dit zijn functies als login, logout, register, change password en dergelijke. In het bestand trivia.py staan de functies die gebruikt worden voor het uitvoeren van het spel. Deze functies zijn create game, process question, show leaderboard en dergelijke. In de map templates staan de html-bestanden van elke webpagina. Design.md is het technisch ontwerp dat gemaakt is voordat er begonnen is met werken aan de website. Trivia.db is de database waarin de vragen worden gegenereerd, scores worden bijgehouden en users worden opgeslagen.

# Taakverdeling

Omdat wij met zijn tweeën aan de website hebben gewerkt, hebben we het grootste gedeelte samen gedaan. Wel heeft Lars iets meer de lay-out van de website op zich genomen en Eric het programmeren van de functies.

# Screenshot Applicatie

[Imgur](https://i.imgur.com/jCZj67s.png)