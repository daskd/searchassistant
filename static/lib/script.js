
$(function() {
	// We want the default behavior of the form, as is on the w3css template, because it shows nice validation messages.
	// But we don't want the form to function in the default way: we will be sending the query to google by our code.

	$('#submitquery').click(function()
		{
			$("#resultsHere").html('');
			window.myquery = $('#querytextbox').val()
			window.mystatus = gatherRulesInOneString('statusitems', 4)
			window.mypreferences = gatherRulesInOneString('preferenceitems', 4)
			
			runMyRoutine();
		});



	$('#submitqueryform').submit(function(event)
		{
			event.preventDefault();
		});
})

function runMyRoutine()
{
	finalquery = window.myquery + ' ' + window.mystatus + ' ' + window.mypreferences;
	$("#resultsHere").load(encodeURI("http://localhost:8084/test/getsearchresultsashtml/?query=" + finalquery));
}


function gatherRulesInOneString(formID, numberOfRules)
{
	statusRules = '';
	ruleElements = getInputElementsArray(formID);
	for (i=0; i<numberOfRules; i++)
		statusRules += ruleElements[i].value + ' '
	return statusRules.trim();
	
}

function getInputElementsArray(formID)
{
	elementsPath = '#' + formID + ' input';
	return $(elementsPath);
}


