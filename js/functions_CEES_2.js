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



document.getElementById('forms_login_btn_submit').addEventListener('click',login);// Adding handler to forms_login_btn_submit button

//document.getElementById('forms_login_btn_clear').addEventListener('click',clear);// Adding handler to forms_login_btn_clear  button

document.getElementById('forms_stores_btn_submit').addEventListener('click',checkin);// Adding handler to forms_stores_btn_submit button

document.getElementById('forms_login_btn_logout').addEventListener('click',checkout);// Adding handler to forms_login_btn_logout button