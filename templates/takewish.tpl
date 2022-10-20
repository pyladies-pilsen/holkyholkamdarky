<h1>Dárkovníček<h1>
<h2>Registrace pro splnění přání</h2>

    <form action="/takewishdone" method="post">
        <input id="id_prani" type="hidden" name="id_prani" value="{{id_prani}}">

       <div class="formrow">

           <div class="formcol">
                <label>Jméno dárce:</label>
                <input id="name" name="name" type="text" required autofocus>
           </div>

           <div class="formcol">
                <label>Kontaktní email:</label>
                <input id="email" name="email" type="email" required>
           </div>

           <div class="formcol">
                <label>Telefon:</label>
                <input id="phone" name="phone" type="text" required>
           </div>

           <div class="formcol">
                  <label>Způsob doručení:</label>
                  <select name="delivery" id="delivery" required>
                      <option>OSOBNĚ do sídla Nadace 700 let města Plzně, Kopeckého sady 11</option>
                      <option>NECHÁM DORUČIT do sídla Nadace 700 let města Plzně, Kopeckého sady 11, 301 00 Plzeň 3</option>
                  </select>
            </div>
        </div>
        <br>
        (Volitelně) Doplňující informace:<br>
        <textarea cols="50" rows="5" id="message" name="message"></textarea>
        <br>
         <input class="submit_button" value="Splnit přání" id="submit" type="submit"><br>

    </form>

    <p>Odesláním těchto údajů vyjadřuji souhlas s těmito GDPR podmínkami:
    Osobní údaje dárců slouží výhradně iniciativě Holky holkám k jejich kontaktování v souvislosti s danou aktivitou,
    do níž se zapojili. Nebudou poskytnuty žádné třetí straně, ani využívány k marketingovým účelům.
    </p>

%rebase templates/base
