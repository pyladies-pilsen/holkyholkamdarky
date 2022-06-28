<h1>Dárkovníček<h1>
<h2>Upload souboru s dárky.</a></h2>

    <div id="message"><p>{{!message}}</p></div>
    <p>Očekáván je soubor ve formátu .xlsx který má data v prvním listu.<br>
    Data jsou ve 4 sloupcích: kód; příjemce, doplňující údaj, přání
    </p>

        <form action="/upload" method="post" enctype="multipart/form-data">
        Přiložete soubor s daty:
            <input type="file" id="upfile" name="upfile">
            <input type="submit" value="Odeslat">
        </form>

    % if defined('content_html'):
        <h2>Nahrány byly tyto záznamy:</h2>
        <div id="content">{{!content_html}}</div>
    % end

<p><a href="/admin">[Návrat na správu dárků]</a></p>

%rebase templates/base
