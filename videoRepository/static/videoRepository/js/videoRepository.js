function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
	// test that a given url is a same-origin URL
	// url could be relative or scheme relative or absolute
	var host = document.location.host; // host + port
	var protocol = document.location.protocol;
	var sr_origin = '/' + host;
	var origin = protocol + sr_origin;
	// Allow absolute or scheme relative URLs to same origin
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	// or any other URL that isn't scheme relative or absolute i.e relative.
	!(/^(\/\/|http:|https:).*/.test(url));
}

function setCookieInHeader(xhr, settings) {
	if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
		// Send the token to same-origin, relative URLs only.
		// Send the token only if the method warrants CSRF protection
		// Using the CSRFToken value acquired earlier
		xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
	}
}

function submitVRForm() {
	var csrfToken = "<input type='hidden' name='csrfmiddlewaretoken' value='" + $.cookie('csrftoken') + "' />"
	$(".VRButton").before(csrfToken);
}

// This function is called from a button and invokes the click action on a file input with the given id,
// which will cause the hidden file input to launch its file dialgo.  The file input is hidden using css.
//  We do all of this because there is no simple way to put css onto an input of type 'file' other than
// to simply hide it.  We are doing it this way instead of using the jQuery $.click() function becuase
// jQueryUI is interfering with that functionality on their buttons. 
function submitFile(hiddenID) {
	// Invokes the file dialog - If the user OKs, the hidden button's .change() function can be invoked in the page
	// javascript file.  (This function is usefule sitewide, but let each hidden button take its own actions.)
	$('#'+hiddenID).click();
}

$(document).ready(function(){
	$.ajaxSetup({ beforeSend:setCookieInHeader });

	$(".VRButton").button();
	$(".VRForm").submit(submitVRForm);
});

