<html>

%if res[0][1] > 1:
        <a href="/oplog">Queue List</a> <p>
%end

<form method="POST" action="/oplog/{{res[0][0]}}/search">
                <input name="sstring"     type="text" />
                <input type="submit" value="search" />
              </form>

<h1>Queue: {{res[0][0]}}</h1>
<b>Date: {{str(res[2][4])}}</b><p>
<a href="/oplog/{{res[0][0]}}/{{res[2][0]}}"> < - Older </a>
%if res[2][3] == 'T':
	| <a href="/oplog/{{res[0][0]}}/{{res[2][2]}}"> Newer -> </a>
%end
<p>
%for i in res[1]['hits']['hits']:
	<h3>{{i['_source']['subject']}}</h3>
	<b>From:</b> {{i['_source']['from']}}<br>
	<b>Sent:</b> {{i['_source']['sent']}}<br>
	<b>Received:</b> {{i['_source']['submitted']}}<p>
	{{i['_source']['body']}}<p>
	--------------------------------------------------------------------<p>
%end
</html>
