var http = require('http');
var ids = [];
var receivedID = ''

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  //Return the url part of the request object:
  var txt = '';
  for (i = 0; i < ids.length; i++) {
  	txt += ids[i];
  	txt += '\n';
  }
  res.write(txt);
  res.end();
}).listen(8080);

var SerialPort = require('serialport');
serialport = new SerialPort("COM5", {
    baudRate: 9600,
    // defaults for Arduino serial communication
    dataBits: 8, 
    parity: 'none', 
    stopBits: 1, 
    flowControl: false 
});
serialport.on('open', function(){
  console.log('Serial Port Opened');
  serialport.on('data', function(data){
  	  var textChunk = data.toString('utf8');
  	  for (i = 0; i < 4; i++) {
	  	  if (textChunk[i] == '&') {
	  	  	receivedID = '';
	  	  }
	  	  else if (textChunk[i] == '$') {
	  	  	for (j = 0; j < ids.length; j++) {
	  	  		if (receivedID != ids[j]) {
	  	  			if (j == (ids.length - 1)) {
	  	  				ids.push(receivedID);
	  	  				console.log(receivedID);
	  	  			}
	  	  			continue;
	  	  		}
	  	  		else {
	  	  			break;
	  	  		}
	  	  	}
	  	  }
	  	  else {
	  	  	receivedID += textChunk[i];
	  	  }
	  }	  
  });
});