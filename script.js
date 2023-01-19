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