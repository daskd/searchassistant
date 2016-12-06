
$(function() {
	// We want the default behavior of the form, as is on the w3css template, because it shows nice validation messages.
	// But we don't want the form to function in the default way: we will be sending the query to google by our code.
	$('#submitqueryform').submit(function(event)
		{
			alert(window.myvalue1);
			event.preventDefault();
		});

	$("#submitquery").click(function()
		{
			window.myvalue1 = $('#statusrules input').eq(0).val()
		});


})
