<html>

<a href="/oplog/{{res[0]}}">Return to {{res[0]}} queue</a> | 
%if res[0][1] > 1:
        <a href="/oplog">Queue List</a> <p>
%end

<form method="POST" action="/oplog/{{res[0]}}/search">
                <input name="sstring"     type="text" />
                <input type="submit" value="search" />
              </form>

<h1>Search Results: {{res[2]}}</h1>
<p>
%count = 1
%for i in res[1]['hits']['hits']:
	%count = count + 1
	<h3>{{!i['_source']['subject']}}</h3>
	<b>From:</b> {{i['_source']['from']}}<br>
	<b>Sent:</b> {{i['_source']['sent']}}<br>
	<b>Received:</b> {{i['_source']['submitted']}}<p>
	<pre>{{!i['_source']['body']}}</pre><p>
	--------------------------------------------------------------------<p>
%end
Total results: {{str(count)}}<p>
</html>
