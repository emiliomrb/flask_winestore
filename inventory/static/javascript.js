$(document).ready(function(){
    var InputsWrapper = $("#InputsWrapper");
    var AddButton = $("#AddField");


    $(AddButton).click(function(){

            $(InputsWrapper).append('<tr><td>{{addwine.wine(class="form-control form-control-lg")}}</td><td>{{addwine.quantity(class="form-control form-control-lg")}}</td><td><button class="btn btn-danger removeclass">-</button></td></tr>')
        });
});

