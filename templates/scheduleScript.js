rides = {'EE' : 'Easy Enduro 1H', 'FT': 'First Timers', '2T': '2T Enduro'}
ridesReverse = {'Easy Enduro 1H': 'EE','First Timers' : 'FT','2T Enduro' : '2T'}

rides2 = ['Easy Enduro 1H','First Timers','2T Enduro'];

var times;
var selectedTime,selectedDay;
$(document).ready(function () {

    if('ontouchstart' in document.documentElement)
        document.body.style.zoom = "30%";

    getSchedule();
    console.log(times)
    createTable();
    fillRides();
    fillInstructors();
  });


function getSchedule(){

    $.ajax({
        type: 'POST',
        url: "/getSchedule",
        context: document.body,
        global: false,
        async:false,
        success: function(data) {
           times = data;
        }
    });
}

function fillRides(){
    //To add the kind of Rides
    const myArray = times[0]

    for (var i = 0; i < myArray.length; i++) {
        var cell = document.getElementById(myArray[i][0].toString() + "&" + myArray[i][1]);
        cell.innerHTML = cell.innerHTML + " " + rides[myArray[i][2]] + "<br>";
    }
    // To add the number of instructors
    // for (var i = 0; i < myArray.length; i++) {
    //     var cell = document.getElementById(myArray[i][0].toString() + "&" + myArray[i][1]);
    //     cell.innerHTML = cell.innerHTML + " " + myArray[i][2];

    // }
}

function fillInstructors(){

    var myArray = JSON.parse(JSON.stringify(times[0]));

    for(var i=0; i< myArray.length; i++)
        myArray[i].splice(2, 1);
    console.log(myArray)
    myArray = myArray.filter((a = {}, b => !(a[b] = b in a)));
    console.log(myArray)
    //To add the number of instructors
    for (var i = 0; i < myArray.length; i++) {
        var cell = document.getElementById(myArray[i][0].toString() + "&" + myArray[i][1]);
        cell.innerHTML = cell.innerHTML + "<br>"  + "INSTRUCTORS:" + myArray[i][2].toString();

    }
}

function createTable(){

        //Fill the table
        var table = document.getElementById("customers");
        // var tbody = table.querySelector('tbody');
        for (var i = 0; i < times[1].length; i++) {
          var row = document.createElement('tr');
          var cells = [];
          var time = document.createElement('td');
          var monday = document.createElement('td');
          monday.id = '1&' + times[1][i];
          monday.classList.add('time_slot');
          var tuesday = document.createElement('td');
          tuesday.id = '2&' + times[1][i];
          tuesday.classList.add('time_slot');
          var wednesday = document.createElement('td');
          wednesday.id = '3&' + times[1][i];
          wednesday.classList.add('time_slot');
          var thursday = document.createElement('td');
          thursday.id = '4&' + times[1][i];
          thursday.classList.add('time_slot');
          var friday = document.createElement('td');
          friday.id = '5&' + times[1][i];
          friday.classList.add('time_slot');
          var saturday = document.createElement('td');
          saturday.id = '6&' + times[1][i];
          saturday.classList.add('time_slot');
          var sunday = document.createElement('td');
          sunday.id = '0&' + times[1][i];
          sunday.classList.add('time_slot');
          var delCell = document.createElement('td');
          var delCellButton = document.createElement('button');
          delCellButton.classList.add('delCellButton','btn','btn-outline-success');
          delCellButton.innerHTML = '-';
          delCell.appendChild(delCellButton);

          time.innerHTML = times[1][i];
          row.appendChild(time);
          row.appendChild(monday);
          row.appendChild(tuesday);
          row.appendChild(wednesday);
          row.appendChild(thursday);
          row.appendChild(friday);
          row.appendChild(saturday);
          row.appendChild(sunday);
          row.appendChild(delCell);

          table.appendChild(row);
        }
}

var cellRides = []
$(document).on('click','.time_slot', function(){

        //Giving information about the cell
        const index = this.parentNode.rowIndex;
        const customersTable = document.getElementById("customers");
        const timeValue = customersTable.rows[index].cells[0].innerHTML;


        document.getElementById("cellToUpdate").innerHTML = "Updating " + customersTable.rows[0].cells[this.cellIndex].innerHTML
        + " " + timeValue;

        const ridesTable = document.getElementById("rides");
        cellRides.length = 0;

        //Set the time and day of the cell selected
        selectedDay = this.id.split('&')[0];
        selectedTime = this.id.split('&')[1];
        cellRides = this.innerHTML.split('<br>');
        let instructorNumber = cellRides.pop().split(':')[1];
        cellRides.pop();

        $('#rides').empty();
        cellRides.map((item) =>{
        let row = document.createElement("tr");
        let cell = document.createElement("td");
        let button = document.createElement("button");
        button.classList.add("removeRideButton");
        let cellButton = document.createElement("td");
        cell.innerHTML = item;
        button.innerHTML = '-';
        button.classList.add('btn','btn-outline-success')
        cellButton.appendChild(button);
        row.appendChild(cell);
        row.appendChild(cellButton);
        ridesTable.appendChild(row);
        });


        let finalrow = document.createElement("tr");
        let finalcell = document.createElement("td");
        let finalbutton = document.createElement("button");
        finalbutton.id = "addRide";
        let finalcellButton = document.createElement("td");
        let finalOptions = document.createElement("select");
        finalOptions.id = "addRideSelect";

        finalcell.appendChild(finalOptions);
        finalbutton.innerHTML = '+';
        finalbutton.classList.add('btn','btn-outline-success')
        finalcellButton.appendChild(finalbutton);
        finalrow.appendChild(finalcell);
        finalrow.appendChild(finalcellButton);
        ridesTable.appendChild(finalrow);


        let filteredArray = []
        //find rides that are not in time slot
        for (var i = 0; i < rides2.length; i++)
            if(!cellRides.includes(" "+ rides2[i]))
                filteredArray.push(rides2[i]);


        finalOptions.length = 0;
        //populate select with option
        for(var i = 0; i < filteredArray.length; i++) {
            var opt = filteredArray[i];
            var el = document.createElement("option");
            el.textContent = opt;
            el.value = opt;
            finalOptions.appendChild(el);
        }

        if(instructorNumber === undefined)
            document.getElementById("instrctNum").value = '0';
        else
            document.getElementById("instrctNum").value = instructorNumber.toString();


});


$(document).on('click','#addRide', function(){

    const selectobject = document.getElementById("addRideSelect");
    if(selectobject.length == 0)
        return
    const rideToAdd = document.getElementById("addRideSelect").value;
    const ridesTable = document.getElementById("rides");
    let row = document.createElement("tr");
    let cell = document.createElement("td");
    let button = document.createElement("button");
    let cellButton = document.createElement("td");
    cell.innerHTML = rideToAdd;
    button.innerHTML = '-';
    button.classList.add('btn','btn-outline-success','removeRideButton')
    cellButton.appendChild(button);
    row.appendChild(cell);
    row.appendChild(cellButton);
    $('#rides tr:last').before(row);

    for (var i=0; i<selectobject.length; i++) {
        if (selectobject.options[i].value == rideToAdd)
            selectobject.remove(i);
    }

    cellRides.push(rideToAdd);

});
$(document).on('click','.removeRideButton', function(){

    //We remove the row from the table
    const index = this.parentNode.parentNode.rowIndex;
    const ridesTable = document.getElementById("rides");
    const rideValue = ridesTable.rows[index].cells[0].innerHTML;
    ridesTable.deleteRow(index);

    //We remove the item from the list of items to be send
    cellRides = cellRides.filter(ride => ride != rideValue);

    //We add the Removed item back to the select
    var el = document.createElement("option");
    el.textContent = rideValue;
    el.value = rideValue;
    document.getElementById("addRideSelect").appendChild(el);
});

$("#submit").on("click", function(){

    if(selectedDay == null || selectedTime == null){
        window.alert("Please select a Day and Time");
        return
    }

    var newCellRides = []

    for(var i=0; i<cellRides.length; i++)
        newCellRides.push(ridesReverse[cellRides[i].trim()]);

    const ridesString = newCellRides.join('+');
    window.location.href = "/updateFromAdmin?cellRides=" + ridesString + "&instructors=" + document.getElementById("instrctNum").value +"&day="
    + selectedDay + "&time=" + selectedTime;
});

$(document).on('click','.delCellButton', function(){

    //Giving information about the cell
    const time = this.parentNode.parentNode.cells[0].innerHTML;
    if (confirm("You are about to delete the time slot: " + time))
        window.location.href = "/deleteTimeRow?time=" + time;

    });
