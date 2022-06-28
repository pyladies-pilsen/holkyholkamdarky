<h1>Dárkovníček<h1>
<h2>Přihlášení do správy dárků.</h2>

    <div id="message"><p>{{message}}</p></div>

        <form action="/login" method="post">
            <!-- Username: <input name="username" type="text" /> -->
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>


%rebase templates/base
