// Get the banner image and the array of image sources
const bannerImage = document.getElementById("image-banner");
const banner = document.getElementById("banner-image");
const bannerImages = ["image1.jpg", "image2.jpg", "image3.jpg"];
const months = {
    "1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June", "7": "July",
    "8": "August", "9": "September", "10": 'October', "11": "November", "12": "December"
  };
const rides = {'EE' : 'Easy Enduro', 'FT': 'First Timers', '2T': '2T Enduro'};
  
// const week = { "1": "Sun", "2": "Mon", "3": "Tue", "4": "Wed", "5": "Thu", "6": "Fri", "7": "Sat" };

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


$(document).ready(function () {

    var date = new Date();

    renderCalendar(date.getMonth()+1, date.getFullYear());
});

function days_between(date1) {

    var date2 = new Date();
    // The number of milliseconds in one day
    const ONE_DAY = 1000 * 60 * 60 * 24;

    // Calculate the difference in milliseconds
    const differenceMs = date1 - date2;

    // Convert back to days and return
    return Math.round(differenceMs / ONE_DAY);

}
function renderCalendar(month,year){

    $(".days").empty();

    //Find how many days the previous month has 
    var previosuMonth = ((month - 1 == 0) ? 12 : month - 1);
    var previousYear = ((month - 1 == 0) ? year - 1 : year);
    var daysInPreviousMonth = new Date(previousYear, previosuMonth, 0).getDate();

    var currYear = year;
    var currMonth = month;
    var dategiven = months[currMonth.toString()] + " " + "1, " + currYear
    var firstDayofThisMonth = new Date(dategiven).getDay();



    //Setting current month and year in calendar
    const currentDate = document.querySelector(".current-date");
    currentDate.innerText = `${months[currMonth]} ${currYear}`;
    currentDate.setAttribute('id',currMonth);

    //Getting last day of month
    var lastDateofMonth = new Date(currYear, currMonth, 0).getDate();

    var ul = document.querySelector(".days");
    var li;

    //Days of previous month
    var StartingPoint = daysInPreviousMonth - firstDayofThisMonth + 1;
    if(firstDayofThisMonth != 0 ){
        for(var i=StartingPoint; i<=daysInPreviousMonth; i++){
            li = document.createElement("li");
            li.innerHTML = i;
            li.setAttribute('class','calendarDay inactive');
            li.setAttribute('id',i);
            ul.appendChild(li);
        }
    }

    var dayActivation;

    //Populate calendar with days
    for(var i=1; i<=lastDateofMonth; i++){
        li = document.createElement("li");
        li.innerHTML = i;
        
        var diff = days_between(new Date(currYear, currMonth - 1, i));
        if((diff > 21) || (diff < 0))
            dayActivation = "inactive";
        else 
            dayActivation = "active";

        li.setAttribute('class','calendarDay ' + dayActivation);
        li.setAttribute('id',i);
        ul.appendChild(li);
    }
}

$("#prev").on("click", function () {
    const currentDate = document.querySelector(".current-date");
    var currMonth = parseInt(currentDate.id);
    var currYear = parseInt(currentDate.innerHTML.split(" ")[1]);

    if (currMonth === 1)
        renderCalendar(12,currYear - 1);
    else
        renderCalendar(currMonth - 1, currYear);


});

$("#next").on("click", function () {
    const currentDate = document.querySelector(".current-date");
    var currMonth = parseInt(currentDate.id);
    var currYear = parseInt(currentDate.innerHTML.split(" ")[1]);


    if (currMonth === 12)
        renderCalendar(1,currYear + 1);
    else
        renderCalendar(currMonth + 1, currYear);


});

var day_to_send;
var month_to_send;
var year_to_send;
// Event listener for options 
var optiondiv = document.querySelector("#options");
var selectedDay = null;

function setCheckoutBtn(){
    var checkOutButton = document.getElementById("checkoutBtn");
    checkOutButton.innerText = '';
    checkOutButton.className = '';
    var redirectElemnt = document.createElement("a");
    redirectElemnt.setAttribute('href', 'checkout.html?day=' + day_to_send + '&month=' + month_to_send + '&year=' + year_to_send );
    redirectElemnt.addEventListener("click", function(event){
        event.preventDefault();
        clickedOnAnchor();
    });
    redirectElemnt.innerText = "Check out";
    redirectElemnt.classList.add("btn","btn-outline-success");
    checkOutButton.appendChild(redirectElemnt);
}

function resetCheckoutBtn(){
    var checkOutButton = document.getElementById("checkoutBtn");
    checkOutButton.replaceChildren();
    checkOutButton.classList.add("disabled", "btn");
    checkOutButton.innerText = 'Check out';
}

$("body").on("click", function(e){
    if(e.target.classList.contains('calendarDay') && e.target.classList.contains('active')){
        
        //Add selected date to template
        day_to_send = e.target.id;
        month_to_send = document.querySelector(".current-date").innerText.split(" ")[0];
        month_to_send_number = document.querySelector(".current-date").id;
        year_to_send = document.querySelector(".current-date").innerText.split(" ")[1];

        const day_of_week_to_send = new Date(year_to_send, month_to_send_number, day_to_send).getDay();
        getDays(day_of_week_to_send);

        // Calendar check selected day
        if(selectedDay != null && selectedDay != e.target)
            //We remove the selected font from the previous date
            selectedDay.classList.remove("clickedDays");

        
        selectedDay = e.target; //Save the new selected day 
        e.target.classList.add("clickedDays");
        optiondiv.classList.add("show");
        document.getElementById("rideHeader").innerHTML = "Your choice is: " + rides[chosenRide];
        setCheckoutBtn();
    }
    else if(!optiondiv.contains(e.target)){
        resetCheckoutBtn();
        optiondiv.classList.remove("show");
    }
});

/*Funciton to toggle the calendar and checkout button upon clicking
on a ride option*/
var chosenRide
$(".ride").on("click", function(e){
    chosenRide = this.id;
    const calendar = document.querySelector("#collapsedCalendar");
    const checkoutBtn = document.querySelector("#checkoutBtn");

    if(calendar.style.opacity == 0){
        calendar.style.opacity = "1";
        checkoutBtn.style.opacity = "1";
        calendar.style.height = "630px";
        checkoutBtn.style.height = "40px";
    }
    else{
        calendar.style.opacity = "0";
        checkoutBtn.style.opacity = "0";
        calendar.style.height = "0px";
        checkoutBtn.style.height = "0px";
    }
});

/*Converting into a POST method and setting the required fields*/
function clickedOnAnchor(){
    

    //  $.post("/checkout", { 'day': day_to_send, 'month': month_to_send, "year":year_to_send, 'ride':chosenRide }, function (data) {
    //     document.write(data);
    //  });
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/checkout", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            window.location.href = '/checkoutComplete';
        }
    }
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ 'day': day_to_send, 'month': month_to_send_number, 'year':year_to_send, 'ride':chosenRide, 
    'time':$("#availableTimeSlots").val(), 'people': $("#numOfPeople").val() }));

};

//Funciton to get available time slots when click on day on the calendar
function getDays(day_of_week_to_send){
    $.post("/getDays", { 'day': day_of_week_to_send, 'ride':chosenRide }, function (result) {
        const selectTag = document.getElementById("availableTimeSlots");
        $("#availableTimeSlots").empty();

        result.map((item) =>{
            let opt = document.createElement("option");
            opt.value = item;
            opt.innerHTML = item;
            selectTag.append(opt);
        })
    }).fail(function(data) {
        console.log(data);
      });

}
