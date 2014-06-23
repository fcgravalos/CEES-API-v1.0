function getCookie(name) {
	console.log(name);
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
			console.log('pasa por el if');
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);

        }
    }
});

function hide_element(id){
 //se obtiene el id
var el = document.getElementById(id); //se define la variable "el" igual a nuestro div
el.style.display = "none" ; //damos un atributo display:none que oculta el div

}

function show_element(id){
 //se obtiene el id
var el = document.getElementById(id); //se define la variable "el" igual a nuestro div
el.style.display = "block" ; //damos un atributo display:block que oculta el div

}

function view_element(id){
 //se obtiene el id
var el = document.getElementById(id); //se define la variable "el" igual a nuestro div
el.style.visibility =  "visible" ; //damos un atributo display:none que oculta el div

}


function login(){

// UI transiction screen

	hide_element ('forms_login');
	show_element ('forms_p_welcome');

// Render the response (stores) on the forms_stores_select_country (select_field)

	//By the momment just show a select field with static content,  further a specific function will add options dinamically to the select field based on the JSON sent by the BE	
	show_element ('forms_stores');

}

function checkin(){
// UI transiction screen

	hide_element ('forms_stores');
	hide_element ('forms_arrivals_img_initial');
	show_element ('forms_img_banner');
    show_element ('forms_logout');

// call to BE to retrieve clients presentes in the store selected


// Render the response (clients) on the forms_arrivals_table_customers (table)

	//By the momment just show a static table further a specific function will build dinamically the table based onthe JSON sent by the BE

	view_element ('forms_arrivals_table_customers');
	
}

function checkout(){
	
// Call to BE to checkuot 

// UI transiction screen

	show_element ('forms_arrivals_img_initial');
    show_element ('forms_login');
	hide_element ('forms_img_banner');
	hide_element ('forms_logout');
	hide_element ('forms_arrivals_table_customers');

}


//-------------------------------------------------------------

$( document ).ready(function() {
	$("#forms_login_btn_submit" ).click(function() {
	
	$( document ).ready(function() {
    $.ajax({
      url:"https://80.240.139.49/shopassistants/login/",
      type:"POST",
      contentType:"application/json; charset=utf-8",
      data:
	  {
			"email":"sa.test@cees.com",
		   	"password":"test1234",
	   		"macAddress":"00:0C:29:18:6C:1A"
	  },
      dataType:"json"
    });
  });
  });
});

//----------------------------------------------------------
//		$("#forms_login_btn_submit" ).click(function() {
//		$("#forms").css("background-color","yellow");
//		$.post("https://80.240.139.49/shopassistants/login/",
//		$.ajax({
//      		url:"http://urlapi/user/login",
//		    type:"POST",
//		    headers: { 
//        		"Accept" : "application/json; charset=utf-8",
//        		"Content-Type": "application/json; charset=utf-8"
//	    },
//      	data:{ username: "pippo", password: "secret123" },
//      	dataType:"json"
//	    })  
//}); 
//   		{
//			"email":"sa.test@cees.com",
//		   	"password":"test1234",
//	   		"macAddress":"00:0C:29:18:6C:1A"
//		},
//	  	function(data, status, json) {
//			 console.log('Data: ' + data + '\nStatus: ' + status);
//		});
//    });
//
//});


//document.getElementById('forms_login_btn_submit').addEventListener('click',login);// Adding handler to forms_login_btn_submit button

document.getElementById('forms_login_btn_clear').addEventListener('click',login);// Adding handler to forms_login_btn_clear  button

document.getElementById('forms_stores_btn_submit').addEventListener('click',checkin);// Adding handler to forms_stores_btn_submit button

document.getElementById('forms_login_btn_logout').addEventListener('click',checkout);// Adding handler to forms_login_btn_logout button