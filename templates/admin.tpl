<h1>Dárkovníček<h1>
<h2>Správa dárků</h2>

<div id="message">
    <p>{{get('message', '')}}</p>
</div>

<div id="content">
    % if defined('content_html'):
        <form action="/adminaction" method="post">
            {{!content_html}}
            <button name="akce" value="change_to_volne" type="submit">Změnit stav na volné.</button>
            <button name="akce" value="change_to_rezervovane" type="submit">Změnit stav na rezervované.</button>
            <button name="akce" value="change_to_vyrizene" type="submit">Změnit stav na vyřízené.</button>
            <br>
            <div title="Jako ochranu před nechtěným smazáním, napište do textového pole, slovo smazat">
                <input type="text" name="delete_confirmation" id="delete_confirmation" placeholder="potvrzení smazání" >
                <button name="akce" value="delete" type="submit" onclick="deleteProtection(this)">Smazat vybraná přání.</button>
            </div>

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
