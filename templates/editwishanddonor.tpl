<h1>Dárkovníček<h1>

<h2 title="Editace id_prani: {{get('id_prani', '')}}">Editace přání a dárce</h2>

<div id="message">
    <p>{{get('message', '')}}</p>
</div>

    <form action="/editwishanddonordone" method="post">
        <input id="id_prani" type="hidden" name="id_prani" value="{{get('id_prani', '')}}">

       <div class="formrow">
           <h2>Přání</h2>
           <div class=="formcol">
                <label>Rok:</label>
                <input id="rok" name="rok" type="number" min="2000" max="2200" value="{{get('rok', '')}}">           
           </div>           

           <div class=="formcol">
                <label>Identifikátor:</label>
                <input id="hh_identifikator" name="hh_identifikator" type="text" value="{{get('hh_identifikator', '')}}">           
           </div>

           <div class=="formcol">
                <label>Příjemce:</label>
                <input id="prijemce" name="prijemce" type="text" value="{{get('prijemce', '')}}">           
           </div>

           <div class=="formcol">
                <label>Věk:</label>
                <input id="doplnujici_udaj" name="doplnujici_udaj" type="text" value="{{get('doplnujici_udaj', '')}}">           
           </div>

           <div class=="formcol">
                <label>Přání:</label>
                <input id="prani" name="prani" type="text" value="{{get('prani', '')}}">           
           </div>

           <div class="formcol">
                  <label>Stav:</label>
                  <select name="stav" id="stav" required>
                      <option>volné</option>
                      <option>rezervované</option>
                      <option>splněno</option>
                  </select>
            </div>

           <hr> 
           <h2>Dárce</h2>
           <p>Dárce je smazán, když jsou zde smazány jeho údaje.</p>
           
           <input id="id_darce" type="hidden" name="id_darce" value="{{get('id_darce', '-1')}}">
            
           <div class="formcol">
                <label>Jméno dárce:</label>
                <input id="name" name="name" type="text" value="{{get('jmeno', '')}}">
           </div>

           <div class="formcol">
                <label>Kontaktní email:</label>
                <input id="email" name="email" type="email" value="{{get('email', '')}}">
           </div>

           <div class="formcol">
                <label>Telefon:</label>
                <input id="phone" name="phone" type="text" value="{{get('telefon', '')}}">
           </div>

           <div class="formcol">
                  <label>Způsob doručení:</label>
                  <select name="delivery" id="delivery">
                      <option>OSOBNĚ do sídla Nadace 700 let města Plzně, Kopeckého sady 11</option>
                      <option>NECHÁM DORUČIT do sídla Nadace 700 let města Plzně, Kopeckého sady 11, 301 00 Plzeň 3</option>
                  </select>
            </div>
        </div>
        <br>
        (Volitelně) Doplňující informace:<br>
        <textarea cols="50" rows="5" id="message" name="message">{{get('zprava', '')}}</textarea>
        <br>
         <input class="submit_button" value="Uložit" id="submit" type="submit"><br>

    </form>

%rebase templates/base
