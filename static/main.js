function caseNum(titles){
    const cases = [2, 0, 1, 1, 1, 2];
    return function(number){
      number = Math.abs(number);
      let c =
       (number%100>4 && number%100<20)? 2 :
          cases[(number%10<5) ? number%10 : 5];
      return  titles[c];
    }
}


$(document).ready(function() {
    const uri = $("#uri").val();
    const seconds = caseNum(['секунду', 'секунды', 'секунд']);
    let i = 4;

    function time(){
        if (i < 0) {
            return;
        }
        --i;
        $("#time").html(i + " " + seconds(i));
        if (i === 0) {
            $.ajax({
                url: "/api/public/link/" + uri,
                dataType: "json",
                method: "POST",
                async: false,
                success: function(result) {
                    console.log("Result: " + result.result);
                    if (result.status === "no"){
                        alert("К сожалению, эта ссылка более не активна :(");
                    }
                    $("#comment").html("Если переадресация не произошла, то <a class='text-warning' href='" + result.result.real_link + "'>нажмите на меня</a>");
                    location.replace(result.result.real_link);
               }
             });

        }
    }
    setInterval(time, 1000);


});
