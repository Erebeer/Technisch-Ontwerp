 #
# Samenvatting
Dit project staat in het teken van het maken van een leuk en leerzaam triviaspel op het internet. Men kan een profiel aanmaken op de website en het spel spelen. Men krijgt een bepaalde tijd om zoveel mogelijk vragen te beantwoorden. Hieraan wordt er een score toegekend waaraan gebruikers zich met elkaar kunnen meten. De ontwikkelaars voor dit spel zijn Lars Bremmers en Eric Louwers.
#
# Features
In ons triviaspel komen de volgende features aan bod.
- Gebruikers kunnen andere gebruikers opzoeken en een connectie maken, oftewel een vriendschapsverzoek sturen
- Gebruikers die bevriend met elkaar zijn kunnen elkaars statistieken zien
- Gebruikers kunnen een categorie selecteren, waarna zij zoveel mogelijk vragen binnen een bepaald tijdsbestek dienen te beantwoorden.
- Bij het spelen van het spel krijgen spelers een bepaalde score per goed beantwoorde vraag. Deze score wordt opgeslagen en kan worden vergeleken.
- Gebruikers kunnen de moeilijkheidsgraad zelf bepalen: easy, medium of hard.
- Er zijn leaderboards beschikbaar: één ten opzichte van je vrienden en één ten opzichte van de rest van de spelers.
- Gebruikers hebben de mogelijkheid met hun vrienden te chatten. Zo kunnen zij in contact met elkaar zijn tijdens het spel.
#
# Minimum Viable product
De minimumeisen van het project zijn als de volgende.
**Gebruikers moeten een profiel kunnen aanmaken**
Gebruikers moeten de mogelijkheid hebben om een profiel aan te maken en in te kunnen loggen. Dit hebben we in ons project verwerkt.
**Er wordt een score toegekend**
Als een gebruiker een Triviaspel speelt, dienen ze een score toegekend te krijgen. Ook dit hebben we in ons project verwerkt met de leaderboards die wij gaan maken.
**Vragen komen uit een online database**
Wij hebben twee databases gevonden waaruit we vragen kunnen halen voor het spel. Deze vragen hebben verschillende moeilijkheidsgraden. Ook dit is in ons project verwerkt.
#
# Afhankelijkheden
Met het maken van de website zijn we afhankelijk van diverse aspecten. Deze aspecten zijn de volgende.
**Databronnen**
[**jService.io**](http://jService.io)
URL: [http://jservice.io/](http://jservice.io/)
[jService.io](http://jService.io) verstrekt, volgens hun website, meer dan 156,800 trivia vragen. Deze vragen hebben verschillende moeilijkheidswaardes (difficulty). Zo zouden wij waardes aan onze moeilijkheidsgraden kunnen toevoegen, waarbij Easy (0-300), Medium (300-700) en Hard (700-1000).
**Trivia Nerd API**
URL: [http://trivia.propernerd.com/](http://trivia.propernerd.com/)
Trivia Nerd heeft veel minder vragen beschikbaar als jService, namelijk maar 191 vragen in totaal. Daarnaast bedraagt de difficulty ook maar waardes van 1-5, en niet van 0-1000. Dit zou wel eens moeilijkheden kunnen veroorzaken bij het implementeren van de API&#39;s.
**Externe componenten**
**Bootstrap**
URL: [https://getbootstrap.com/](https://getbootstrap.com/)
Bootstrap is aantrekkelijk om te gebruiken, aangezien het een groot deel van de last van een website te programmeren van de schouders haalt. Op de site zelf worden 3 zogeheten &quot;themes&quot;, oftewel templates aangeboden. Deze kosten echter $99 per stuk. Dat lijkt ons iets te duur. Gelukkig worden er op allerlei andere websites wel gratis templates aangeboden.
**Vergelijkbare websites**
**Trivia.fyi.**
Een site waarbij je meteen triviavragen krijgt in combinatie met plaatjes. Er is echter geen optie om de vragen te beantwoorden, je kan de antwoorden enkel opvragen. Men kan hierbij geen profiel aanmaken en er zit dus ook geen online spelelement in.
[**Sporcle.com**](http://Sporcle.com)
Een grote website waarbij je verschillende trivia-spellen kunt spelen. Je kan een account aanmaken en quizzen spelen. Iedere gebruiker kan een quiz maken en die indelen op zijn of haar eigen manier. Dit kan variëren tot multiple choice, open vragen, visuele vragen en nog veel meer. Leaderboards worden bijgehouden, de site heeft een eigen community waarin men kan discussiëren, men kan badges winnen en vrienden toevoegen en uitdagen tot een bepaalde quiz. [Sporcle.com](http://Sporcle.com) is een zeer complete trivia spelsite.
[**Triviaplaza.com**](http://Triviaplaza.com)
Op de homepage van [triviaplaza.com](http://triviaplaza.com) dien je een categorie uit te kiezen. Eenmaal gekozen kan men een quiz selecteren en die gaan spelen. Het zijn simpele multiple choice vragen, 10 stuks per quiz. Men kan hierop geen profiel aanmaken, ze kunnen simpelweg hun score testen tegen de gemiddelde score.
#
# Moeilijkste delen
**Implementeren van de API**
Het implementeren van de API lijkt ons vrij lastig. Niet zozeer het toevoegen van aan de websites, maar meer de aanpassingen die er bij komen kijken. Hiermee bedoelen wij de gradaties van de moeilijkheid, de verschillende vragen die wij wel of niet willen toevoegen et cetera.
**Leaderboards**
Het toevoegen van leaderboards is een mooi idee, maar niet het makkelijkste idee. Hierbij zouden alle scores moeten worden opgeslagen in de database en daaronder worden gefilterd op de beste scores. Deze scores zouden dan in een lijst worden weergeven, gesorteerd op van hoog naar laag. Daarnaast zouden wij ook nog een leaderboard voor vrienden willen toevoegen, dus als het ware dat er twee leaderboards zijn. Hierbij kan de gebruiker zien wie van zijn vrienden de beste onderling is.
**Vriendensysteem**
Het lijkt ons een leuk idee dat de gebruiker ook vrienden kan toevoegen. Hiermee kan hij zien of hij betere scores heeft dan de rest. Een chatfunctie zou daarbij ook heel handig zijn, maar dat is een idee voor op het laatst.
Wij verwachten dat er genoeg tutorials zijn te vinden op Google of Youtube. voor deze moeilijkste delen.
**Update 17-1-2018**
We hebben na het creëren van het technisch ontwerp besloten om het vriendensysteem opzij te leggen. Dit zou een idee kunnen zijn voor later als de minimale eisen zijn voldaan. 
Daarnaast hebben wij besloten om, indien de gebruiker het vraagt, het wachtwoord op te sturen naar de desbetreffende e-mail. Hiervoor hebben wij gekozen, wegens het wellicht wat lastiger kan worden om links te gaan versturen om het wachtwoord te veranderen. 
