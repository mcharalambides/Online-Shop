var personalInfoFlag = false;
$("#personlInfo").on("click", function(e){
    const dateSelected = document.getElementById("personlInfoCollapse");

    if(personalInfoFlag){
        dateSelected.style.height = "1px";
        personalInfoFlag = false;
    }
    else{
        dateSelected.style.height = "200px";
        personalInfoFlag = true;
    }


});

$("#dateSelected").on("click", function(e){
    const dateSelected = document.getElementById("dateSelectedCollapse");

    if(personalInfoFlag){
        dateSelected.style.height = "0px";
        dateSelected.style.padding = "0px";
        personalInfoFlag = false;
    }
    else{
        dateSelected.style.height = "200px";
        dateSelected.style.padding = "5px";
        personalInfoFlag = true;
    }


});