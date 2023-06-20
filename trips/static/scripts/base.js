
$.get("https://ipinfo.io", function (response) {
    $('#search-field').attr("placeholder",response.city)
}, "jsonp");

const registerbutton = document.getElementsByClassName('register-wrapper')[0];
const login_button = document.querySelector('#sign-in');
const close_login_button = document.querySelector('.close-login')
const reg_btns = document.querySelectorAll('.register-options a');
const close_reg_button = document.querySelector('.close-register')

reg_types = ["tourist","guide","tour_agent","tourist","guide","tour_agent"]

login_button.addEventListener('click', function () {
    document.getElementsByClassName('login-wrapper')[0].style = "display:flex"
})

close_login_button.addEventListener('click', function () {

        document.getElementsByClassName('login-wrapper')[0].style = "display:none"

})

reg_btns.forEach(function (item, index) {
    item.addEventListener('click', function () {
            document.getElementsByClassName('register-wrapper')[0].style = "display:flex"
            document.cookie = 'type='+reg_types[index]
    })
})

close_reg_button.addEventListener('click', function () {
    document.getElementsByClassName('register-wrapper')[0].style = "display:none"
    document.cookie = 'type='+reg_types[0]

})

$(document).mouseup(function (e){ 
    var div1 = $(".login-wrapper"); 
    if (div1.is(e.target) 
        && div1.has(e.target).length === 0) { 
        div1.hide();
    }
    var div2 = $(".register-wrapper");
    if (div2.is(e.target) 
        && div2.has(e.target).length === 0) {
            div2.hide(); 
            document.cookie = 'type='+reg_types[0]
    }
});

function showRegister() {
    $('.register-wrapper .form-wrapper').toggle(400);
    $('.register-wrapper .social-button').toggle(400)
    $('.register-wrapper .or-line').toggle(400)
}
$('.register-wrapper .email-register-button').click(function () {
    showRegister()
})



// Switch from links
document.querySelector('.login-wrapper .switch').addEventListener('click', switchToReg)
document.querySelector('.register-wrapper .switch').addEventListener('click', switchToLog)

function switchToReg() {
    document.getElementsByClassName('login-wrapper')[0].style = "display:none"
    document.getElementsByClassName('register-wrapper')[0].style = "display:flex"
}

function switchToLog() {
    document.getElementsByClassName('login-wrapper')[0].style = "display:flex"
    document.getElementsByClassName('register-wrapper')[0].style = "display:none"
    document.cookie = 'type='+reg_types[0]
}

function livesearch(element) {
    let list = document.getElementById("hints")
    if (element.value.length >= 3){
      let val = element.value

     $.ajax({
      url: "/live_search/",
      type: "GET",
      data: {"query":val},
      success: function (data) {
        
         list.innerHTML = ""
         let i = 0;
         for(var key in data){
           list.innerHTML += "<li onclick='setValue(this)'>" + data[key] + "</li>" 
           i++;
           if(i>5){
             break
           }
         }
      },
    });
  }else{
    list.innerHTML = ""
  }
  }
  function setValue(elem){
    $("#search-field").val(elem.innerText)
    $("#search").submit()
  }