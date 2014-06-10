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

function submit_login (){

	hide_element ('forms_login');
	show_element ('forms_p_welcome');
	show_element ('forms_stores');
	
}

function submit_stores (){

	hide_element ('forms_stores');
	hide_element ('forms_arrivals_img_initial');
	view_element ('forms_arrivals_table_customers');
	show_element ('forms_img_banner');
    show_element ('forms_logout');
	
}
