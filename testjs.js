var PythonShell = require('python-shell');

var options = {
  scriptPath: './'
};

var pyshell = new PythonShell('testfile.py',options);

pyshell.on('message', function (message) {
  // received a message sent from the Python script (a simple "print" statement) 
  console.log(message);
});

// end the input stream and allow the process to exit 
pyshell.end(function (err) {
  if (err) throw err;
  console.log('finished');
});