<html>
%for i in res['hits']['hits']:
	<h3>{{i['_source']['subject']}}</h3>
	<b>From:</b> {{i['_source']['from']}}<br>
	<b>Sent:</b> {{i['_source']['sent']}}<br>
	<b>Received:</b> {{i['_source']['submitted']}}<p>
	{{i['_source']['body']}}<p>
	--------------------------------------------------------------------<p>
%end
</html>
