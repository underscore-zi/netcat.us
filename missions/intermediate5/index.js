var app = require('express')();
app.use(require('morgan')('dev'));
var session = require('express-session');
var FileStore = require('session-file-store')(session);
app.use(session({
  name: 'server-session-cookie-id',
  secret: 'bvue8cyrcb37acy872b62c7bo8z2s6zs8671cb7826c4o8c27o7c2tv8tc82y8c4o7sby87cvsts52',
  saveUninitialized: true,
  resave: true,
  store: new FileStore()
}));

var svgCaptcha = require('svg-captcha');

app.get('/', function (req, res) {
	res.status(200).send("/captcha for the captcha... /captcha_submit to submit answer. submit answer within 1000 milliseconds to get the flag.");
});
app.get('/captcha', function (req, res) {
    var captcha = svgCaptcha.create({'noise':4});
    req.session.captcha = captcha.text;
    var d = new Date();
	var n = d.getTime();
	req.session.starttime = n;
    res.set('Content-Type', 'image/svg+xml');
    res.status(200).send(captcha.data);
});

app.get('/captcha_submit', function (req, res) {
	var d = new Date();
	var n = d.getTime();

	if ((n - req.session.starttime) > (1 * 1000)) {
		res.status(400).send("400 - U Took 2 Long")
	} else if (req.session.captcha) {
		//Accessed within allowed time!
		//Verify solution...
		var solu = req.query.answer;
		if (!solu) {
			res.status(400).send("Please specify you answer to the CAPTCHA in the 'answer' field of the GET request to this page.");
			return;	
		}
		if (solu == req.session.captcha) {

			//SOLVED
			//Show Flag
			res.set('Content-Type', 'text/html');
			res.status(200).send("<h1>Password is <code>xMosaku55</code></h1>");
 			return;
		} else {
			res.status(400).send("YOU FAILED!");
			return;
		}

	} else {
		res.set('location', '/captcha');
		res.status(302).send("302 - No CAPTCHA shown yet.");

	}
});

app.listen(8765, function () {
  console.log('Captcha app listening on port 8765!')
})
