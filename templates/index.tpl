<h1>Dárkovníček<h1>
<h2>Organizovaný <a href="https://HolkyHolkamPlzen.cz">Holky holkám Plzeň</a></h2>
<div id="content">

    % if defined('content_html'):
        <form action="/takewish" method="post">
            {{!content_html}}
        </form>
    % else:
        <p>
            <strong>
                Děkujeme za podporu, aktuálně zde nemáme žádná nesplněná přání.<br>
            </strong>
        </p>
    % end

    <p>
        Pokud chcete být informováni, když přibudou nová přání, zašlete nám svůj email.<br>
        TODO: Formulář pro registraci emailu zájemce.
    </p>
</div>

%rebase templates/base
