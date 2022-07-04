<h1>Dárkovníček<h1>
<h2>Registrace pro splnění přání</h2>

        <form action="/takewishdone" method="post">
            <input id="id_prani" type="hidden" name="id_prani" value="{{id_prani}}">
            Jméno dárce: <input id="name" name="name" type="text" required autofocus><br>
            Kontaktní email: <input id="email" name="email" type="email" required><br>
            Telefon: <input id="phone" name="phone" type="text" required><br>
            Způsob doručení TODO zjisit skutečné způsoby doručení:
            <select name="delivery" id="delivery" required>
                <option>Osobně na pobočku v Plzni.</option>
                <option>Zašlu poštou na pobočku.</option>
                <option>Nechám doručit na pobočku.</option>
            </select><br>
            (Volitelně) Doplňující informace: <textarea cols="30" rows="5"></textarea><br>
            <input value="Splnit přání" id="submit" type="submit"><br>
        </form>

        <p>Odesláním těchto údajů vyjadřuji souhlas s GDPR podmínkami. TODO: Odkaz na GDPR podmínky.</p>


%rebase templates/base
