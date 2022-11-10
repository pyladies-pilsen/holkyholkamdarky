<!--
<h1>Dárkovníček<h1>
<h2>Organizovaný skupinou <a href="https://HolkyHolkamPlzen.cz">Holky&nbsp;holkám&nbsp;Plzeň</a></h2>
-->
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
        Pokud chcete být informováni, až zde přidáme nová přání, zašlete nám zprávu na holkyholkamplzen@centrum.cz<br>
    </p>

</div>

%rebase templates/base
