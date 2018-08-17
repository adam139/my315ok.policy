
require([
  'jquery','bootstrap-carousel','bootstrap-tabs'
], function($,carousel,tabs) {
  'use strict';
$(document).ready(function(){ 
	$(".nav-tabs a").mouseover(function (e) {
		  e.preventDefault();
		  $(this).tab('show');
		});
	$(".nav-tabs").on("click","a",function (e) {
		  e.preventDefault();
		  var url = $(this).attr("data-js-target");
		  window.location.href = url;
		  return false;
		});
    $('.carousel').carousel();
	var existnav = $('.portletNavigationTree');
	if (existnav !== undefined) {            
		var leftHeight = $('.portletNavigationTree dd').height();
		var rightHeight = $('#content').parent().height();
		if((leftHeight) && leftHeight > rightHeight) {
			leftHeight = rightHeight;
			$('.portletNavigationTree dd').height(leftHeight).css("overflow","auto");
		}
	}        
	});
});