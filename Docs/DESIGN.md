
# Technisch ontwerp

Lars Bermmers, Eric Louwers, IK09

### Modules en veelgebruikte hulpfuncties

**Modules die we nodig denken te hebben:**

**Flask:** Om de website op te draaien, de routes naar de verschillende templates te bepalen en de gebruiker gegevens in te laten voeren, gebruikers in te kunnen loggen en ingelogd te blijven.

**passlib.apps:** Om een veilig wachtwoord op te kunnen slaan.

**CS50 → SQL:** Om SQL te kunnen gebruiken in onze codes.

**HTML:** Om html te kunnen programmeren communiceren met html. De templates zullen in html geschreven worden.

**Time:** Module die ervoor zorgt dat je een klok kan gebruiken die de tijd bijhoudt. Zo kunnen we de countdown inzetten.

**Hulpfuncties die we verwachten veel te gebruiken:**

**Error()**: Een functie vergelijkbaar met apology() van Finance. Deze functie wordt uitgevoerd als er iets verkeerds door de gebruiker wordt ingevoerd.

**Login\_required():** De functie die altijd loopt als de gebruiker is ingelogd. Om een spel te kunnen spelen, vrienden te kunnen zoeken, hun wachtwoord te willen veranderen en dergelijke dient de gebruiker ingelogd te zijn.

**Overige hulpmiddelen**

**Countdown Clock:** Een countdown generator die je zelf kunt aanpassen op tijd en lay-out.

        Url: [https://codepen.io/mattlitzinger/pen/ysowF](https://codepen.io/mattlitzinger/pen/ysowF)

**Email pagina bouwen:** Een website die stap voor stap uitlegt hoe je een email template in         html kunt bouwen.

url: [https://webdesign.tutsplus.com/articles/build-an-html-email-template-from-scratch--webdesign-12770](https://webdesign.tutsplus.com/articles/build-an-html-email-template-from-scratch--webdesign-12770)

**Frameworks die we gaan gebruiken**

Wij willen onder andere bootstrap gaan gebruiken. We hebben er allebei nog geen ervaring mee, maar dat kan altijd opgedaan worden. Dit framework zal waarschijnlijk wat meer werk op zich nemen, wat ons dus een voordeel geeft.

_Bootstrap_

[https://getbootstrap.com/](https://getbootstrap.com/)

### Login

**Model**

**Login():** Deze functie gaan wij gebruiken voor het inloggen van de gebruiker. Hierbij checkt het systeem of de ingevulde informatie overeenkomt met de informatie in de database.

**Control**

Method: POST

Functie: login()

@app.route: &quot;/Login&quot;

** **

**View**

Template: login.html

Velden: Username, Password

Knoppen: Login, Forgot Password?, Register

### Wachtwoord vergeten?

**Model**

**Forgotpassword():** Deze functie wordt aangeroepen als de gebruiker zijn wachtwoord is vergeten en deze opgestuurd wenst te krijgen. De gebruikersnaam dient zijn of haar username in te vullen, gevolgd door zijn of haar e-mail adress. De functie controleert of de username bestaat en of het e-mail adress gekoppeld is aan de username (deze staat in de SQL database). Als het klopt, wordt er een email verzonden naar de gebruiker met het wachtwoord. Als het niet klopt, krijgt de gebruiker een error door de errorfunctie.

**Control**

Method: POST

@app.route: &quot;/forgot&quot;

** **

**View**

Template 1: forgotpassword.html

                   Velden: Username, E-mailadress

                   Knoppen: Send Email, Back to login

Template 2: confirmation\_forgotpassword.html

                   Velden: -

                   Knoppen: Back to homepage

### Registratie

**Model**

**Register():**Deze functie slaat de ingevulde informatie op in de database, zodat de gebruiker na zichzelf te registreren zichzelf verder kan inloggen. De functie controleert of alle informatie juist is ingevuld en geeft een error als er bijvoorbeeld dezelfde username al is gebruikt.

**Control**

Methode = POST

@app.route: &quot;/register&quot;

**View**

Template: register.html

                   Velden: Username, E-mailadress, Password, Confirm Password

                   Knoppen: Register, Back to login

### Profiel

**Model**

**profile\_index():** Print informatie voor de gebruiker.

**Change\_password():** Deze functie verandert het wachtwoord voor de gebruiker. Hierbij controleert de functie wel of het oude wachtwoord juist is ingevuld.

**Control**

Methode: GET, POST

@app.route: &quot;/profile&quot;

  **View**

Template 1: profile.html

                   Velden: Username, E-mail adress

                   Knoppen: Friends, Settings, Personal information, Leaderboards, Contact, About us,  Username

Template 2: settings.html

                   Velden: Old password, new password, confirm new password

        Knoppen: Personal information, Friends, Apply

Template 3: personal\_information.html

                   Velden: Number of games played, Number of friends, Total score, Average score(?)

                   Knoppen: Profile, Settings

### Logout

**Model**

**Logout():** Deze functie logt de gebruiker uit (session.clear()) Hierbij zal de functie _Login\_required():_ niet meer van toepassing zijn. De gebruiker zal nadat deze functie is uitgevoerd weer opnieuw moeten inloggen.

**Control**

Method: -

Route: @app.route:&quot;/homepage&quot;

**View**

Template: logout.html

                   Velden:

                   Knoppen: Back to homepage

###  Spel instellen

**Model**

**Setgame():** De gebruiker dient eerst de gewenste difficulty te geven. Vervolgens kiest de gebruiker de gewenste tijd die hij of zij hiervoor wilt gebruiken. Hierbij wordt de variabele &quot;difficulty&quot; vastgesteld. Hiermee wordt de variabele &quot;time&quot; gesteld. Vervolgens dient de gebruiker op de knop &quot;play&quot; te drukken, waarna de variabelen worden opgehaald.

        De variabele &quot;difficulty&quot; wordt gebruikt om de juiste categorie op te vragen van de API, waardoor de API enkel vragen selecteert van de juiste categorie. De variabele &quot;time&quot; geeft de klok weer. Deze loopt af gedurende het spel. Als de gebruiker een van de twee instellingen vergeet aan te klikken krijgt deze een error-melding dmv de functie error().

**Control**

Route: @app.route:&quot;/index&quot;

Method: POST

**View**

Template 1: index.html

        Velden: -

        Knoppen: Play, Select difficulty (Novice, Medium, Hard), Select time (1 minute, 5   minutes, 10 minutes), Leaderboards, About us, Contact, Username

### Spel spelen

**Model**

**game():** Deze functie accepteert een input van de gebruiker. Als het antwoord overeenkomt met het antwoord wat in het systeem staat, krijgt de gebruiker een score van +100. Als de speler het antwoord niet weet, krijgt de speler een score van -100 of -50 wanneer hij de pass knop gebruikt.

**Control**

Route: @app.route:&quot;/game&quot;

Methode: POST

**View**

Template 1: game.html

        Velden: Answer

        Knoppen: Username, notifications, Pass

### Leaderboards

**Model**

_Index():_

Deze functie geeft bepaalde informatie weer voor de gebruiker. Hierbij zal de opgevraagde informatie worden weergegeven op het scherm van de gebruiker.

**Control**

Route: @app.route:&quot;/leaderboards&quot;

Methode: GET

**View**

Template: leaderboards.html

                   Velden: Name, number of games played, Total score, Average score

                   Knoppen: Sort, leaderboards, contact, about us, notifications

### **Contact**

**Model**

**mail():** Wellicht kunnen wij een bepaalde functie creëren zodat gebruikers een e-mail kunnen versturen met daarin opgegeven informatie/vragen. Er bestaan hier ook HTML-codes voor, dus dit zal onwaarschijnlijk zijn dat we het gaan maken.

**Control**

Route: @app.route:&quot;/contact&quot;

Methode: POST

**View**

Template:contact.html

                   Velden: Name, E-mail adress, information

Knoppen: Send, Leaderboards, Contact, About us, Username

### About us

**Model**

Voor deze webpagina is geen functie of code die gebruikt wordt. Enkel routes worden weergegeven.

**Control**

Route: @app.route:&quot;/about&quot;

Methode: -

**View**

Template:about.html

                   Velden: -

Knoppen: Leaderboards, Contact, About us, Username


# Navigatie routes webpagina's

![Imgur](https://i.imgur.com/yVHfYxr.png)