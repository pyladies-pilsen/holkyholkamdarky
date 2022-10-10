<h1>Dárkovníček<h1>
<h2>Registrace pro splnění přání</h2>

        <form action="/takewishdone" method="post">
            <input id="id_prani" type="hidden" name="id_prani" value="{{id_prani}}">
            Jméno dárce: <input id="name" name="name" type="text" required autofocus><br>
            Kontaktní email: <input id="email" name="email" type="email" required><br>
            Telefon: <input id="phone" name="phone" type="text" required><br>
            Způsob doručení TODO zjisit skutečné způsoby doručení:
            <select name="delivery" id="delivery" required>
                <option>OSOBNĚ do sídla Nadace 700 let města Plzně, Kopeckého sady 11</option>
                <option>NECHÁM DORUČIT do sídla Nadace 700 let města Plzně, Kopeckého sady 11, 301 00 Plzeň 3</option>
            </select><br>
            (Volitelně) Doplňující informace: <textarea cols="30" rows="5" id="message" name="message"></textarea><br>
            <input value="Splnit přání" id="submit" type="submit"><br>
        </form>

        <p>Odesláním těchto údajů vyjadřuji souhlas s těmito GDPR podmínkami:
        Osobní údaje dárců slouží výhradně iniciativě Holky holkám k jejich kontaktování v souvislosti s danou aktivitou,
        do níž se zapojili. Nebudou poskytnuty žádné třetí straně, ani využívány k marketingovým účelům.
        </p>

%rebase templates/base
