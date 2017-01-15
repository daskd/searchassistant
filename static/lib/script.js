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
			var rules = $('#rulesdefinition').val();
			setDomain(rules);
		});
	
	// Functionality for 'Submit Domain Query' button
	$('#submitdomainquery').click(function()
		{
			var query = $('#querytextbox').val();
			submitDomainQuery(query);
		});

})

function setDomain(rules)
{
	$('#rulesubmissionresult').val('')
	$.ajax({
		type: 'POST',
		url: '/test/setdomain',
		data: {
			'rules': rules
		},
		success: function (data) {
			$('#rulesubmissionresult').text('Rules submitted successfully. New Domain ID: ' + data);
			window.domainID = data;
		},
		error: function(xhr, textStatus, errorThrown) {
	    	$('#rulesubmissionresult').text('Rule submission failed');
		}
		
	 });
	

}

function submitDomainQuery(query)
{
	domainID = window.domainID;
	if (!domainID)
	{
		alert('You must first submit a set of rules');
		return;
	}

	$('#queryubmissionresult').val('')
	$.ajax({
		type: 'POST',
		url: '/test/querydomain',
		data: {
			'query': query,
			'domainid': domainID
		},
		success: function (data) {
			$('#queryubmissionresult').text('Query submitted successfully. Conclusion: ' + data);
		},
		error: function(xhr, textStatus, errorThrown) {
			$('#queryubmissionresult').text('Query submission failed');
		}
		
	 });
	

}


function runMyRoutine()
{
	var finalquery = window.myquery + ' ' + window.mystatus + ' ' + window.mypreferences;
	$("#resultsHere").load(encodeURI("/test/getsearchresultsashtml/?query=" + finalquery));
}


function gatherRulesInOneString(formID, numberOfRules)
{
	var statusRules = '';
	var ruleElements = getInputElementsArray(formID);
	for (i=0; i<numberOfRules; i++)
		statusRules += ruleElements[i].value + ' '
	return statusRules.trim();
	
}

function getInputElementsArray(formID)
{
	var elementsPath = '#' + formID + ' input';
	return $(elementsPath);
}


