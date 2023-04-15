var sortfield;
var isSorted = true;
$("#adminfilters").on("click",function(){
    var firstName = document.getElementById("firstName").value;
    var lastName = document.getElementById("lastName").value;
    var dateFrom = document.getElementById("dateFrom").value;
    var dateTo = document.getElementById("dateTo").value;

    $.post("/adminfilters",{'firstName': firstName, 'lastName':lastName, 'dateFrom':dateFrom, 'dateTo':dateTo}, function (result) {
        isSorted = false;
        filltable(result[0]);
        document.getElementById("page").innerHTML = result[1] + 1;
    }).fail(function(data) {
        console.log(data);
      });

});

 $('#instructorLeave').on('click', function(){
    var dateFrom = document.getElementById('dateFromInstructor').value;
    var dateTo = document.getElementById('dateToInstructor').value;

    $.post("/instructorLeave",{'dateFrom': dateFrom, 'dateTo':dateTo}, function () {
        
    }).then(function(){
        alert("Succes");
    })
    .fail(function(data) {
        console.log(data);
      });
 });

function dateFormat(date, index){
    var newdate = new Date(date);
    var month = ((newdate.getMonth() < 9) ? '0' + (newdate.getMonth() + 1).toString() : (newdate.getMonth() + 1));
    var day = ((newdate.getDate() < 9) ? '0' + (newdate.getDate()).toString() : (newdate.getDate()));
    if (index == 3)
        return   day + "-" + month + "-" + newdate.getFullYear().toString() + " " + newdate.getUTCHours() + ":" + newdate.getUTCMinutes() + ":" + newdate.getUTCSeconds();
    else
        return   day + "-" + month + "-" + newdate.getFullYear().toString();
    ;
}


$(document).ready(function () {

// Execute a function when the user presses a key on the keyboard
$("input").on("keypress", function(event) {
  // If the user presses the "Enter" key on the keyboard
  if (event.key === "Enter" && ($('#firstName').is(':focus') || $('#lastName').is(':focus') || $('#dateFrom').is(':focus') || $('#dateto').is(':focus')) ) {
    // Cancel the default action, if needed
    // Trigger the button element with a click
    document.getElementById("adminfilters").click();
  }
});
});

$('.pageMarker').on('click', function(){
    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;
    const dateFrom = document.getElementById("dateFrom").value;
    const dateTo = document.getElementById("dateTo").value;
    
    $.get("/nextPage",{'firstName': firstName, 'lastName':lastName, 'dateFrom':dateFrom, 'dateTo':dateTo, 'procedure':this.id}, function (result) {
        filltable(result[0]);
        document.getElementById("page").innerHTML = result[1] + 1;
    }).fail(function(data) {
        console.log(data);
      });

});

function filltable(result){
        var html;
        $("#customers tr").after().remove();
        for(var i = 0; i < result.length; i++){
                html += '<tr><td>' + result[i][0].toString() + '</td><td>' + result[i][7].toString() + '</td>'
                +'<td>' + result[i][8].toString() + '</td><td>' + result[i][2].toString() + '</td>'
                +'<td>' + dateFormat(result[i][4].toString()) + '</td><td>' + result[i][5].toString() + '</td>'
                +'<td>' + result[i][6].toString() + '</td><td>' + result[i][9].toString() + '</td>'
                +'<td>' + result[i][10].toString() + '</td><td>' + dateFormat(result[i][13].toString()) + '</td>'
                +'<td>' + result[i][11].toString() + '</td><td>' + result[i][12].toString() + '</td>'
                +'<td>' + result[i][14].toString() + '</td><td>' + dateFormat(result[i][3].toString(), 3) + '</td></tr>';
        }
        $('#customers tbody').before('<tr><th>id</th><th>First Name</th><th>Last Name</th><th>Ride</th><th id="datetoRide" class="sortFilter">Date to Ride</th><th>Time</th>'+
            '<th>Number of People</th><th>Email</th><th>Telephone</th><th>Date of Birth</th><th>Ethnicity</th><th>Residence</th><th>Driving License</th>'+
            '<th id="dateofOrder" class="sortFilter">Date Of Order</th></tr>');
        $('#customers tbody').after(html);

        if(isSorted){
            if( sortfield === 'dateofOrder'){
                document.getElementById(sortfield).style.backgroundColor = '#797777';
                document.getElementById('datetoRide').style.backgroundColor = '#adadad'; 
            }
            if( sortfield === 'datetoRide'){
                document.getElementById(sortfield).style.backgroundColor = '#797777';
                document.getElementById('dateofOrder').style.backgroundColor = '#adadad';
            } 
        }
};

$("body").on("click",".sortFilter", function(){

    sortfield = this.id;
    isSorted = true;
    $.post("/sortfilters",{'field':this.innerHTML}, function (result) {
        filltable(result);
    }).fail(function(data) {
        console.log(data);
      });

});

$(".sortFilter").on("click", function(){

    sortfield = this.id;
    isSorted = true;
    $.post("/sortfilters",{'field':this.innerHTML}, function (result) {
        filltable(result);
    }).fail(function(data) {
        console.log(data);
      });

});