<h1>Dárkovníček<h1>
<h2>Správa dárků</h2>

<div id="content">
    % if defined('content_html'):
        <form action="/admin" method="post">
            {{!content_html}}
        </form>
    % else:
        <p>
            <strong>
                Aktuálně zde, pro tento rok nejsou žádná přání. Nejspíš bude potřeba nahrát soubor s přáními.<br>
            </strong>
        </p>
    % end
</div>

<p><a href="/upload">[Nahrát soubor s daty]</a></p>
<p><a href="/logout">[Odhlášení]</a></p>

%rebase templates/base
