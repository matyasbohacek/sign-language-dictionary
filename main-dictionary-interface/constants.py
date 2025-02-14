
LOGO_PATH_URL = ""

CONTACT_EMAIL = ""

HEAD_HTML = """
<title>ASL Dictionary</title>

<script>
    gradioURL = window.location.href;
      if (!gradioURL.endsWith('?__theme=light')) {
        window.location.replace(gradioURL + '?__theme=light');
      }
</script>
"""

DESCRIPTION_HTML = f"""
<img src="{LOGO_PATH_URL}" style="width: 120px; margin-left: -5px;">
<h1 style="color: #F7B832; font-family: GraphikBold;">ASL Dictionary</h1>

<b>

<details>
    <summary style="font-size: 1em !important; font-family: GraphikBold;" class="unselectable">
        <b>Instructions</b>
    </summary>
    <br>
    <ol style="font-family: Graphik;  font-weight: 400;">
        <li> Upload or record a video.
        <ul>
            <li> Ensure that there is only a single person in the shot.
            <li> The signer should be front-facing and have a calm background.
        </ul>
       <li> Click "Submit".
       <li> Results will appear in "Results" panel on the right shortly.
       <li> A confidence label is shown next to each prediction, corresponding to the percentual likelihood of the respective sign: 66-100% to Probably, 33-66% to Possibly, and 0-33% to Unlikely.
   </ol>
</details>

<br>

<details style="font-family: Graphik; font-weight: 400;">
    <summary style="font-size: 1em !important; font-family: GraphikBold;" class="unselectable">
    <b>Privacy</b>
    </summary>
    <br>
    We do not collect any user information. The videos are deleted from our servers after the inference is completed, unless you flag any of them for further inspection.
</details>
"""

COMPACT_RESULTS_HTML = f"""
    <div style="padding: 5%;">
    
        $WARNING_MESSAGE$

        <p style="opacity: 0.5; margin-bottom: -20px;">Top prediction</p>
        <br>
        <div style="display:inline-block; width: 100%;">
            <h1 style="display:inline-block; font-size: 2em; font-family: GraphikBold;"><b>$TOP_PRED_CLASS$</b></h1>
            <h1 style="float: right; display:inline-block; font-size: 1.7em; font-family: Graphik;">$TOP_PRED_CONF$</h1>
        </div>
        <p>$DESCRIPTION$</p>
        
        <br>
        
        <img src="$GIF_PATH$" style="width: 100%">
        
        <br>
        
        <hr style="margin-top: 5px; margin-bottom: 5px;">
        
        <p style="opacity: 0.5;">Runner-up predictions</p>
        
        <div style='display: flex; justify-content: space-between; align-items: center;'> $ALTERNATIVES_TABLE_1$ </div>
        <div style='display: flex; justify-content: space-between; align-items: center;'> $ALTERNATIVES_TABLE_2$ </div>
        <div style='display: flex; justify-content: space-between; align-items: center;'> $ALTERNATIVES_TABLE_3$ </div>
        
        
        <p style="opacity: 0.5;">See full analysis for more details.</p>
        <br>
        
        <div style="display:inline-block;">
            <button class="lg primary svelte-cmf5ev" onclick="window.location.replace('$URL$')" >More results</button>
            <!--<button class="gr-button gr-button-lg gr-button-secondary"  style="margin-left: 8px !important;" onclick="window.location.href='{CONTACT_EMAIL}'">Report a problem</button>-->
        </div>
        
    </div>
"""

FORCE_LIGHT_MODE_JS_SCRIPT = """
window.location.replace(window.location.href + '?__theme=light');

window.addEventListener('load', function () {
    console.log("happy happy happy");
  gradioURL = window.location.href;
  if (!gradioURL.endsWith('?__theme=light')) {
    window.location.replace(gradioURL + '?__theme=light');
  }
});
"""

GLOSS = ['DOG', 'DOG', 'DOG', 'DOG', 'GIRAFFE', 'CAT', 'CAT', 'CAT', 'BEE', 'BEE', 'COW', 'TURTLE', 'HORSE', 'ELEPHANT',
         'RABBIT', 'RABBIT', 'BEAR', 'PIG', 'CROCODILE', 'DUCK', 'DUCK', 'SQUIRREL', 'DEER', 'ROOSTER', 'LOBSTER',
         'LOBSTER', 'LOBSTER', 'TIGER', 'ZEBRA', 'LION', 'SNAKE', 'SHARK', 'SHARK', 'WHALE', 'SHRIMP', 'FISH', 'MONKEY',
         'HIPPO', 'HIPPO', 'DONKEY', 'FROG', 'EGG', 'PIZZA', 'PIZZA', 'BACON', 'SAUSAGE', 'TOAST', 'ONION', 'MILK',
         'MILK', 'CHEESE', 'SPAGHETTI', 'SALT', 'HAMBURGER', 'PEPPER', 'FRENCH FRIES', 'COFFEE', 'BREAD', 'TEA',
         'SALAD', 'SANDWICH', 'SANDWICH', 'SANDWICH', 'SANDWICH', 'LETTUCE', 'LETTUCE', 'GRAPES', 'GRAPES', 'TOMATO',
         'STRAWBERRY', 'STRAWBERRY', 'STRAWBERRY', 'STRAWBERRY', 'MEAT', 'MEAT', 'ORANGE', 'POTATO', 'BANANA', 'BANANA',
         'BANANA', 'BANANA', 'BEANS', 'APPLE', 'MELON', 'CAKE', 'CHERRY', 'CHERRY', 'PIE', 'PINEAPPLE', 'PINEAPPLE',
         'PINEAPPLE', 'PINEAPPLE', 'PINEAPPLE', 'COOKIE', 'AMERICA', 'AUSTRALIA', 'SWITZERLAND', 'ISRAEL', 'CANADA',
         'JAPAN', 'CHINA', 'EGYPT', 'FRANCE', 'GERMANY', 'GREECE', 'PUERTORICO', 'GUATEMALA', 'PAKISTAN', 'URUGUAY',
         'PHILIPPINES', 'AUSTRIA', 'NIGERIA', 'MOROCCO', 'TRINIDAD', 'JAMAICA', 'COLOMBIA', 'LEBANON', 'BULGARIA',
         'BANGLADESH', 'IRAQ', 'NICARAGUA', 'CHILE', 'ENGLAND', 'NETHERLANDS', 'SYRIA', 'UNITED STATES', 'SCOTLAND',
         'TIBET', 'PALESTINE', 'PANAMA', 'PORTUGAL', 'VIETNAM', 'TURKEY', 'ARGENTINA', 'NEW ZEALAND.MP4', 'UKRAINE',
         'DOMINICAN REPUBLIC', 'JORDAN', 'NORWAY', 'IRELAND', 'NEW ZEALAND', 'PERU', 'ECUADOR', 'FINLAND', 'BOTSWANA',
         'ICELAND', 'BELIZE', 'ROMANIA', 'HONDURAS', 'KENYA', 'SPAIN', 'TAIWAN', 'INDONESIA', 'POLAND', 'SOUTH AFRICA',
         'IRAN', 'MEXICO', 'HONG KONG', 'NIAMBIA', 'KOREA', 'SAUDI ARABIA', 'SWEDEN', 'CUBA', 'VENEZUELA', 'DENMARK',
         'INDIA', 'MALAYSIA', 'ITALY', 'BOLIVIA', 'PARAGUAY', 'BELGIUM', 'COSTARICA', 'THAILAND', 'EL SALVADOR',
         'RUSSIA', 'SRI LANKA', 'CZECH REPUBLIC']

POTENTIAL_WARNING_MESSAGE = """
<div style="background-color: rgba(255, 165, 0, 0.6); padding: 15px; margin-bottom: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); border-left: 5px solid rgba(255, 140, 0, 0.7);">
    <p style="margin: 0 0 10px 0; text-align: left; font-family: GraphikBold;">
        Warning: Low video quality may affect the accuracy of sign language predictions.
    </p>
    <div style="color: white; padding: 10px; border-radius: 4px; font-family: Graphik;">
        <ul style="margin: 10px 0 0 20px; padding: 0; list-style-type: disc; font-family: Graphik;">
            <li>Ensure good lighting and minimal clutter in the background;</li>
            <li>Be in the center of the frame, with all your gestures visible;</li>
            <li>Allow maximum webcam quality.</li>
        </ul>
    </div>
</div>
"""

NO_RESPONSE_MESSAGE = """
<div style="padding: 5%;"><div style="background-color: rgba(255, 0, 0, 0.4); padding: 15px; margin-bottom: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); border-left: 5px solid rgba(200, 0, 0, 0.7);">
    <p style="margin: 0 0 10px 0; text-align: left; font-family: GraphikBold;">
        No video provided — please try again
    </p>
    <div style="color: white; padding: 10px; border-radius: 4px; font-family: Graphik;">
        <ul style="margin: 10px 0 0 20px; padding: 0; list-style-type: disc; font-family: Graphik;">
            <li>Record a video directly in the browser or upload a video from your computer.</li>
            <li>You can select the desired data source in the lower part of the left panel.</li>
            <li>To record a video or choose a file, click on the left panel.</li>
        </ul>
    </div>
</div>
</div>
"""