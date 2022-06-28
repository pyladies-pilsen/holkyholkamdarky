<h1>Dárkovníček<h1>
<h2>Registrace pro splnění přání</h2>

        <form action="/" method="post">
            Jméno dárce: <input name="darce" type="text /><br>
            Kontaktní email: <input name="email" type="text" /><br>
            (Volitelně) telefon: <input name="telefon" type="text"/><br>
            Způsob doručení:
            <select name="delivery">
                <option>Osobně na pobočku v Plzni.</option>
                <option>Zašlu poštou na pobočku.</option>
                <option>Nechám doručit na pobočku.</option>
            </select><br>
            (Volitelně) Doplňující informace: <textarea cols="30" rows="5"></textarea><br>
            <input value="Splnit přání" type="submit" /><br>
        </form>


%rebase templates/base
