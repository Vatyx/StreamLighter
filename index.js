var express = require('express');
var app = express();
app.use(express.static('public'));
app.use(express.static('files'));

var options = {
  mode: 'text',
  pythonOptions: ['-u'],
};

var PythonShell = require('python-shell');
var pyshell = new PythonShell("main2.py", options);

// PythonShell.run('main2.py', options, function (err, results) {
// 	  if (err) throw err;
// 	  // results is an array consisting of messages collected during execution
// 	  console.log("'results: %j', results");
// 	  console.log("Executed!")
// 	});

var path = require('path');
var mime = require('mime');
var fs = require('fs');
var bodyParser = require('body-parser')
app.use( bodyParser.json() );
app.use(bodyParser.urlencoded({ extended: true }));

var highlight = false;
var download = false;
var gettingdownload = false;

var downloadname = "";


app.get('/', function (req, res) {
	setTimeout(function() {}, 2000);
	res.sendfile('index.html');
});

app.post('/startrecording', function(req, res)
{
	console.log("starting to record");
	var streamname = req.body.name;
	recording = true;
	console.log(streamname)
	pyshell.send(streamname)
	res.end();
})

app.get('/update', function(req, res)
{
	payload = {};
	if(highlight == false)
	{
		payload = {status: "recording"};
	}
	else if(highlight == true && download == false && gettingdownload == false)
	{
		payload = {status: "highlight_start"};
	}
	else if(highlight == true && download == true && gettingdownload == false)
	{
		payload = {status: "highlight_end"}
	}
	else if(highlight == true && download == true && gettingdownload == true)
	{
		payload = {status: "download"};

		highlight = false;
		download = false;
		gettingdownload = false;
	}

	res.json(payload);
});

app.get('/download', function(req, res)
{
	var file = __dirname + '/' + downloadname;

	res.download(file);
});

pyshell.on('message', function (message) {
  // received a message sent from the Python script (a simple "print" statement)
  console.log("In message which was: " + message);

  if(message == "~~~Highlight start set!~~~")
  {
  	console.log("Highlight start")
  	highlight = true;
  }
  else if(message == "~~~Highlight end~~~")
  {
  	console.log("Highlight end")
  	download = true;
  }
  else if(message.substring(0, 9) == "highlight")
  {
  	console.log("Highlight download")
  	gettingdownload = true;
  	downloadname = message;
  }

});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
})