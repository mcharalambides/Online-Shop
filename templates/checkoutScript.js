$(document).ready(function () {
    populateCountries(countryList);
    birthday = document.getElementById("birthday");
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = yyyy + '-' + mm + '-' + dd;

    birthday.max = birthday.value = today

    today  = new Date(new Date().setFullYear(new Date().getFullYear() - 100));
    vdd = String(today.getDate()).padStart(2, '0');
    mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    yyyy = today.getFullYear();
    today = yyyy + '-' + mm + '-' + dd;

    birthday.min = today;

    document.getElementById('dateSelected').click();
    document.getElementById('personlInfo').click();


});

var personalInfoFlag = false;
$("#personlInfo").on("click", function(){
    const dateSelected = document.getElementById("personlInfoCollapse");

    if(personalInfoFlag){
        dateSelected.style.height = "1px";
        personalInfoFlag = false;
    }
    else{
        if($(window).height() < 415)
            dateSelected.style.height = "55vh";
        else
            dateSelected.style.height = "20vh";
        personalInfoFlag = true;
    }


});

var dateSelectedFlag = false;
$("#dateSelected").on("click", function(){
    const dateSelected = document.getElementById("dateSelectedCollapse");

    if(dateSelectedFlag){
        dateSelected.style.height = "0px";
        dateSelected.style.padding = "0px";
        dateSelectedFlag = false;
    }
    else{
        if($(window).height() < 415)
        dateSelected.style.height = "55vh";
        else
        dateSelected.style.height = "23vh";

        dateSelected.style.padding = "5px";
        dateSelectedFlag = true;
    }
// $("input").on("invalid", function(){
//     this.setCustomValidity("Please Give a Value");
// });

// $("input").on("valid", function(){
//     this.setCustomValidity("");
// });

});
function populateCountries(countryList){
    const ethnicity =  document.getElementById("ethnicity");
    const residence =  document.getElementById("residence");
    countryList.map((item) =>{
    let opt1 = document.createElement("option");
    let opt2 = document.createElement("option");
    opt1.value = item;
    opt2.value = item;
    opt1.innerHTML = item;
    opt2.innerHTML = item;
    ethnicity.append(opt1);
    residence.append(opt2);
})
};


$(window).on('resize', function(){
    document.getElementById('dateSelected').click();
    document.getElementById('personlInfo').click();

    if($(window).height < 400){
        $('h1').style.fontSize = '1rem';
    }

});