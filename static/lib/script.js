
$(function() {
	// We want the default behavior of the form, as is on the w3css template, because it shows nice validation messages.
	// But we don't want the form to function in the default way: we will be sending the query to google by our code.

	$('#submitquery').click(function()
		{
			window.myquery = $('#qquery').val()
			window.myrules = gatherRulesInOneString('statusrules', 4)
			
			runMyRoutine();
		});



	$('#submitqueryform').submit(function(event)
		{
			alert('User query: ' + window.myquery);
			alert('User additional rules: ' + window.myrules);
			event.preventDefault();
		});
})

function runMyRoutine()
{
	$("#resultsHere").load("http://www.google.com");
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


