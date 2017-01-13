// On Load
$(function() {
	// We want the default behavior of the form, as is on the w3css template, because it shows nice validation messages.
	// But we don't want the form to function in the default way: we will be sending the query to google by our code.

	// Functionality for 'Submit Query' button
	$('#submitquery').click(function()
		{
			$("#resultsHere").html('');
			window.myquery = $('#querytextbox').val()
			window.mystatus = gatherRulesInOneString('statusitems', 4)
			window.mypreferences = gatherRulesInOneString('preferenceitems', 4)
			
			runMyRoutine();
		});


	// Arrangement for the form to not be sent in the regular way
	// (we call our service by ajax)
	$('#submitqueryform').submit(function(event)
		{
			event.preventDefault();
		});


	// Functionality for 'Submit Rules' button
	$('#submitrules').click(function()
		{
			rules = $('#rulesdefinition').val();
			setDomain(rules);
		});

})

function setDomain(rules)
{
	$.ajax({
		type: 'POST',
		url: '/test/setdomain',
		data: {
			'rules': rules
		},
		success: function (data) {
			//alert('Domain ID: '+data);
			alert('worked !');
			alert(data);
		},
		error: function(xhr, textStatus, errorThrown) {
	       alert('Request failed');
		}
		
	 });
	

}


function runMyRoutine()
{
	finalquery = window.myquery + ' ' + window.mystatus + ' ' + window.mypreferences;
	$("#resultsHere").load(encodeURI("/test/getsearchresultsashtml/?query=" + finalquery));
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


