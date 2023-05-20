//Define Header and Footer
var countryList = [
	"Afghanistan",
	"Albania",
	"Algeria",
	"American Samoa",
	"Andorra",
	"Angola",
	"Anguilla",
	"Antarctica",
	"Antigua and Barbuda",
	"Argentina",
	"Armenia",
	"Aruba",
	"Australia",
	"Austria",
	"Azerbaijan",
	"Bahamas (the)",
	"Bahrain",
	"Bangladesh",
	"Barbados",
	"Belarus",
	"Belgium",
	"Belize",
	"Benin",
	"Bermuda",
	"Bhutan",
	"Bolivia (Plurinational State of)",
	"Bonaire, Sint Eustatius and Saba",
	"Bosnia and Herzegovina",
	"Botswana",
	"Bouvet Island",
	"Brazil",
	"British Indian Ocean Territory (the)",
	"Brunei Darussalam",
	"Bulgaria",
	"Burkina Faso",
	"Burundi",
	"Cabo Verde",
	"Cambodia",
	"Cameroon",
	"Canada",
	"Cayman Islands (the)",
	"Central African Republic (the)",
	"Chad",
	"Chile",
	"China",
	"Christmas Island",
	"Cocos (Keeling) Islands (the)",
	"Colombia",
	"Comoros (the)",
	"Congo (the Democratic Republic of the)",
	"Congo (the)",
	"Cook Islands (the)",
	"Costa Rica",
	"Croatia",
	"Cuba",
	"Curaçao",
	"Cyprus",
	"Czechia",
	"Côte d'Ivoire",
	"Denmark",
	"Djibouti",
	"Dominica",
	"Dominican Republic (the)",
	"Ecuador",
	"Egypt",
	"El Salvador",
	"Equatorial Guinea",
	"Eritrea",
	"Estonia",
	"Eswatini",
	"Ethiopia",
	"Falkland Islands (the) [Malvinas]",
	"Faroe Islands (the)",
	"Fiji",
	"Finland",
	"France",
	"French Guiana",
	"French Polynesia",
	"French Southern Territories (the)",
	"Gabon",
	"Gambia (the)",
	"Georgia",
	"Germany",
	"Ghana",
	"Gibraltar",
	"Greece",
	"Greenland",
	"Grenada",
	"Guadeloupe",
	"Guam",
	"Guatemala",
	"Guernsey",
	"Guinea",
	"Guinea-Bissau",
	"Guyana",
	"Haiti",
	"Heard Island and McDonald Islands",
	"Holy See (the)",
	"Honduras",
	"Hong Kong",
	"Hungary",
	"Iceland",
	"India",
	"Indonesia",
	"Iran (Islamic Republic of)",
	"Iraq",
	"Ireland",
	"Isle of Man",
	"Israel",
	"Italy",
	"Jamaica",
	"Japan",
	"Jersey",
	"Jordan",
	"Kazakhstan",
	"Kenya",
	"Kiribati",
	"Korea (the Democratic People's Republic of)",
	"Korea (the Republic of)",
	"Kuwait",
	"Kyrgyzstan",
	"Lao People's Democratic Republic (the)",
	"Latvia",
	"Lebanon",
	"Lesotho",
	"Liberia",
	"Libya",
	"Liechtenstein",
	"Lithuania",
	"Luxembourg",
	"Macao",
	"Madagascar",
	"Malawi",
	"Malaysia",
	"Maldives",
	"Mali",
	"Malta",
	"Marshall Islands (the)",
	"Martinique",
	"Mauritania",
	"Mauritius",
	"Mayotte",
	"Mexico",
	"Micronesia (Federated States of)",
	"Moldova (the Republic of)",
	"Monaco",
	"Mongolia",
	"Montenegro",
	"Montserrat",
	"Morocco",
	"Mozambique",
	"Myanmar",
	"Namibia",
	"Nauru",
	"Nepal",
	"Netherlands (the)",
	"New Caledonia",
	"New Zealand",
	"Nicaragua",
	"Niger (the)",
	"Nigeria",
	"Niue",
	"Norfolk Island",
	"Northern Mariana Islands (the)",
	"Norway",
	"Oman",
	"Pakistan",
	"Palau",
	"Palestine, State of",
	"Panama",
	"Papua New Guinea",
	"Paraguay",
	"Peru",
	"Philippines (the)",
	"Pitcairn",
	"Poland",
	"Portugal",
	"Puerto Rico",
	"Qatar",
	"Republic of North Macedonia",
	"Romania",
	"Russian Federation (the)",
	"Rwanda",
	"Réunion",
	"Saint Barthélemy",
	"Saint Helena, Ascension and Tristan da Cunha",
	"Saint Kitts and Nevis",
	"Saint Lucia",
	"Saint Martin (French part)",
	"Saint Pierre and Miquelon",
	"Saint Vincent and the Grenadines",
	"Samoa",
	"San Marino",
	"Sao Tome and Principe",
	"Saudi Arabia",
	"Senegal",
	"Serbia",
	"Seychelles",
	"Sierra Leone",
	"Singapore",
	"Sint Maarten (Dutch part)",
	"Slovakia",
	"Slovenia",
	"Solomon Islands",
	"Somalia",
	"South Africa",
	"South Georgia and the South Sandwich Islands",
	"South Sudan",
	"Spain",
	"Sri Lanka",
	"Sudan (the)",
	"Suriname",
	"Svalbard and Jan Mayen",
	"Sweden",
	"Switzerland",
	"Syrian Arab Republic",
	"Taiwan",
	"Tajikistan",
	"Tanzania, United Republic of",
	"Thailand",
	"Timor-Leste",
	"Togo",
	"Tokelau",
	"Tonga",
	"Trinidad and Tobago",
	"Tunisia",
	"Turkey",
	"Turkmenistan",
	"Turks and Caicos Islands (the)",
	"Tuvalu",
	"Uganda",
	"Ukraine",
	"United Arab Emirates (the)",
	"United Kingdom of Great Britain and Northern Ireland (the)",
	"United States Minor Outlying Islands (the)",
	"United States of America (the)",
	"Uruguay",
	"Uzbekistan",
	"Vanuatu",
	"Venezuela (Bolivarian Republic of)",
	"Viet Nam",
	"Virgin Islands (British)",
	"Virgin Islands (U.S.)",
	"Wallis and Futuna",
	"Western Sahara",
	"Yemen",
	"Zambia",
	"Zimbabwe",
	"Åland Islands"
];
class MyHeader extends HTMLElement {
    connectedCallback(){
        this.innerHTML  =`
        <header>
        <nav style="width:80%" class="navbar navbar-expand-lg navbar-light">
          <div class="container-fluid">
            <div class="collapse navbar-collapse container-fluid justify-content-center" id="navbarScroll">
              <div style="padding-right: 40px;">
                <a class="navbar-brand" href="/">
                  <div class="logo-image">
                        <img src="../static/Logo.jpeg" class="img-fluid">
                  </div>
                </a>
              </div>
              <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
                <li class="nav-item">
                  <a class="nav-link active" aria-current="page" href="/">Home</a>
                </li>`+
                /*<li class="nav-item">
                  <a class="nav-link" href="#">2T Enduro</a>
                </li>*/
                `<li class="nav-item dropdown">
				<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Rides
                  </a>
                  <ul style="position: absolute;" class="dropdown-menu" aria-labelledby="navbarScrollingDropdown">
					<li><a class="dropdown-item" href="https://www.sayiousadventurepark.com/first-timers-course/">First Timers</a></li>
					<li><a class="dropdown-item" href="https://www.sayiousadventurepark.com/enduro-tours-beginners/">Easy Enduro</a></li>
					<li><a class="dropdown-item" href="https://www.sayiousadventurepark.com/enduro-tour-experts/intermediate/">2T Enduro</a></li>

                  </ul>
                </li>`+
                // <li class="nav-item">
                //   <a class="nav-link" href="#" tabindex="-1" aria-disabled="true">First Timers</a>
                // </li>
				`{% if session['user'] %}
			  <li class="nav-item">
			  <a class="nav-link" href="/userProfile" tabindex="-1" aria-disabled="true">Profile</a>
			</li>
			{% endif %}
		  </ul>` +
            //   <div style="padding-left:60px;">
            //     <button class="btn btn-outline-success" type="submit">BOOK NOW</button>
            //   </div>
			`
              {% if not session['user'] %}
              <div style="padding-left:60px;">
              <a id="loginBtn" class="btn btn-outline-success" href="login.html">LOGIN</a>
              </div>
              {% endif %}
              {% if session['user'] %}
              <div style="padding-left:60px;">
              <a id="logoutBtn" class="btn btn-outline-success" href="/logoutUser">LOGOUT</a>
              </div>
              {% endif %}
              {% if not session['user'] %}
              <div style="padding-left:20px;">
              <a id="registerBtn" class="btn btn-outline-success" href="register.html">REGISTER</a>
              </div>
              {% endif %}
              </div>
            </div>
          </div>
        </nav>
      </header>`
    }
}

class MyFooter extends HTMLElement {
    connectedCallback(){
        this.innerHTML  =`
        <footer class="bg-light py-3">
        <div class="container">
          <p class="text-center">Copyright &copy;2023 Sayious Adventure Park</p>
          <div class="d-flex justify-content-center">
            <a class="footerElement" href="https://www.enduroridescyprus.com/terms-conditions1">Terms of Service</a>
            <a class="footerElement" href="https://www.enduroridescyprus.com/terms-conditions1">Privacy Policy</a>
            <a class="footerElement" href="https://www.sayiousadventurepark.com/contact">Contact Us</a>
          </div>
        </div>
      </footer>`
    }
}


customElements.define('my-header', MyHeader);
customElements.define('my-footer', MyFooter);
