// Get the banner image and the array of image sources
const bannerImage = document.getElementById("image-banner");
const banner = document.getElementById("banner-image");
const bannerImages = ["image1.jpg", "image2.jpg", "image3.jpg"];

const months = {
    "1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June", "7": "July",
    "8": "August", "9": "September", "10": 'October', "11": "November", "12": "December"
  };

// Set the initial banner image
let currentBanner = 0;
bannerImage.src = bannerImages[currentBanner];

// Function to change the banner image
function changeBanner() {
  currentBanner++;
  if (currentBanner === bannerImages.length) {
    currentBanner = 0;
  }
  bannerImage.classList.add("change-banner");
  setTimeout(() => {
    banner.src = bannerImages[currentBanner];
    bannerImage.classList.add("slide-in");
    setTimeout(() => {
        bannerImage.classList.remove("change-banner");
        bannerImage.classList.remove("slide-in");
    }, 500);
  }, 500);
}

// Set the interval to change the banner image
//setInterval(changeBanner, 5000); // change the banner every 5 seconds

//Define Header and Footer

class MyHeader extends HTMLElement {
    connectedCallback(){
        this.innerHTML  =`
        <header>
        <nav class="navbar navbar-expand-lg navbar-light">
          <div class="container-fluid">
            <div class="collapse navbar-collapse container-fluid justify-content-center" id="navbarScroll">
              <div style="padding-right: 40px;">
                <a class="navbar-brand" href="/">
                  <div class="logo-image">
                        <img src="Logo.png" class="img-fluid">
                  </div>
                </a>
              </div>
              <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
                <li class="nav-item">
                  <a class="nav-link active" aria-current="page" href="#">Home</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#">2T Enduro</a>
                </li>
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#" id="navbarScrollingDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Easy Enduro
                  </a>
                  <ul class="dropdown-menu" aria-labelledby="navbarScrollingDropdown">
                    <li><a class="dropdown-item" href="#">Action</a></li>
                    <li><a class="dropdown-item" href="#">Another action</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#">Something else here</a></li>
                  </ul>
                </li>
                <li class="nav-item">
                  <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">First Timers</a>
                </li>
              </ul>
              <div style="padding-left:60px;">
                <button style = "color: #accaac; font-weight: 500; background-color: #1d7d07;" class="btn btn-outline-success" type="submit">BOOK NOW</button></div>
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
          <p class="text-center">Copyright &copy;2021 Online Shop</p>
          <div class="d-flex justify-content-center">
            <a href="#">Terms of Service</a>
            <a href="#">Privacy Policy</a>
            <a href="#">Contact Us</a>
          </div>
        </div>
      </footer>`
    }
}

customElements.define('my-header', MyHeader);
customElements.define('my-footer', MyFooter);

$(document).ready(function () {

    var date = new Date();

    renderCalendar(date.getMonth()+1, date.getFullYear());


});

function renderCalendar(month,year){

    $(".days").empty();

    currYear = year;
    currMonth = month;

    //Setting current month and year in calendar
    const currentDate = document.querySelector(".current-date");
    currentDate.innerText = `${months[currMonth]} ${currYear}`;
    currentDate.setAttribute('id',currMonth);

    //Getting last day of month
    var lastDateofMonth = new Date(currYear, currMonth, 0).getDate();

    var ul = document.querySelector(".days");
    var li;

    for(var i=1; i<=lastDateofMonth; i++){
        li = document.createElement("li");
        li.innerHTML = i;
        li.setAttribute('class','calendarDay');
        ul.appendChild(li);
    }
}

$("#prev").on("click", function () {
    const currentDate = document.querySelector(".current-date");
    var currMonth = parseInt(currentDate.id);
    var currYear = parseInt(currentDate.innerHTML.split(" ")[1]);

    console.log(currMonth, currYear);

    if (currMonth === 1)
        renderCalendar(12,currYear - 1);
    else
        renderCalendar(currMonth - 1, currYear);


});

$("#next").on("click", function () {
    const currentDate = document.querySelector(".current-date");
    var currMonth = parseInt(currentDate.id);
    var currYear = parseInt(currentDate.innerHTML.split(" ")[1]);

    console.log(currMonth, currYear);

    if (currMonth === 12)
        renderCalendar(1,currYear + 1);
    else
        renderCalendar(currMonth + 1, currYear);


});

// Event listener for options 
var optiondiv = document.querySelector("#options");

$("body").on("click", function(e){
    if(e.target.className == 'calendarDay')
        optiondiv.classList.add("show");
    else if(!optiondiv.contains(e.target))
        optiondiv.classList.remove("show");
});
