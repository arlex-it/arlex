const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const cors = require('cors');
const autoIncre = require('mongoose-auto-increment');
const request = require('request');
const AutoIncrement = require('mongoose-sequence')(mongoose);
const nodemailer = require('nodemailer');
var ip = require('ip');

var options = {
	keepAlive: 300000,
	connectTimeoutMS: 30000,
	useNewUrlParser: true
};

const app = express();
app.use(cors());

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

mongoose.connect("mongodb://corentin:corentin98@ds239055.mlab.com:39055/api_proto_arlex", options);
const db = mongoose.connection;
// autoIncre.initialize(db);
db.on('error', console.error.bind(console, 'Erreur lors de la connexion'));
db.once('open', function (){
	console.log("Connexion à la base OK");
});


let productSchema = new mongoose.Schema({
	id: Number,
	ean: String,
	dlc: String
});

productSchema.plugin(AutoIncrement, {inc_field: 'id'});
var product = mongoose.model('products', productSchema);

let userSchema = new mongoose.Schema({
	name: String,
	prod: {type: Array, default: []}
});

var users = mongoose.model('users', userSchema);


let transporter = nodemailer.createTransport({
	service: "Gmail",
	auth: {
		user: "arlex.proto@gmail.com",
		pass: "Epitech21!"
	}
});

let mailOptions = {
	to: "arlex.proto@gmail.com",
	subject: Date() + " - Nouvelle Ip serveur pour proto arlex",
	html: "<h1>Coucou copain</h1>Voici l'ip : http://" + ip.address() + ":8080"
};
transporter.sendMail(mailOptions);


app.get('/infos', function (req, res) {
	product.find(function (err, prod) {
		if (err)
			return res.json({err: err});
		res.status(200).json(prod);
	});
});

app.get('/infos/:id', function (req, res) {
	let id = req.params.id;
	console.log("on demande l'id ", id);
	product.findOne({id: id}, function (err, item) {
		if (err)
			return res.json({err: err});
		if (!item)
			return res.json({err: "None"});
		request(`https://fr.openfoodfacts.org/api/v0/produit/${item.ean}.json`, function (err, resp, body) {
			if (err)
				return res.json({err: err});
			body = JSON.parse(body).product;
			let name = body.product_name_fr;
			let allergens = body.allergens_from_ingredients;
			let traces = body.traces;
			res.json({dlc: item.dlc, name: name, allergens: allergens, traces: traces});
		});
	})
});

app.delete('/delete/:id', function (req, res) {
	let id = req.params.id;
	console.log("on demande l'id ", id);
	product.findOneAndDelete({id: id}, function (err, item) {
		if (err)
			return res.json({err: err});
		if (!item)
			return res.json({err: "None"});
		res.json({succ: "success"});
	})
});

app.put('/modif/:id', function (req, res) {
	let id = req.params.id;
	console.log("on demande l'id ", id);
	product.findOne({id: id}, function (err, item) {
		if (err)
			return res.json({err: err});
		if (!item)
			return res.json({err: "None"});
		item.ean = req.body.ean || item.ean;
		item.dlc = req.body.dlc || item.dlc;
		item.save();
		res.json("OK!");
	});
});

app.post('/add', function (req, res) {
	let pro = new product({
		ean: req.body.ean,
		dlc: req.body.dlc || "Aucune"
	});
	pro.save();
	res.json('Ok');
});

app.post('/user/add', function(req, res) {
	let user = req.body.user;
	let name = req.body.name;
	let etage = req.body.etage;
	let id = req.body.id;

	console.log("on st ici");
	users.findOne({name: user}, function (err, item_user) {
		if (err)
			res.json({err: err});
		product.findOne({id: id}, function (err, item) {
			if (err)
				return res.json({err: err});
			if (!item)
				return res.json({err: "None"});
			request(`https://fr.openfoodfacts.org/api/v0/produit/${item.ean}.json`, function (err, resp, body) {
				if (err)
					return res.json({err: err});
				body = JSON.parse(body).product;

				let name_prod = body.product_name_fr;

				let n_prod = id + '|' + name_prod + '|' + name + '|' + etage;

				if (item_user) {
					let prod = item_user.prod;
					let idx = 0;
					let find = false;
					prod.forEach(function (elem) {
						let infos = elem.split('|');
						if (infos[0] === id) {
							prod[idx] = n_prod;
							item_user.prod = prod;
							find = true;
							users.findOne({name: user}, function (err, test) {
								test.prod = prod;
								test.save(function (err) {
									if (err)
										console.log("EROOOOOR SAVE WTF");
									console.log("on save")
									return res.json({data: "Its ok!", prod: test.prod});
								});
							});

						}
						idx += 1;
					});

					if (!find) {
						item_user.prod.push(n_prod);
						item_user.save();
						return res.json({data: "Ok new"});
					}
				}
				else {
					item_user = new users;
					item_user.name = user;
					item_user.prod.push(n_prod);
					item_user.save();
					res.json({data: "Ok new USER"});
				}
			});
		});

	});
});

app.post('/user/search', function (req, res) {
	let name = req.body.prod.toLowerCase();
	let user = req.body.user;

	users.findOne({name: user}, function (err, item) {
		if (err)
			res.json({err: err});
		if (item) {
			let prod = item.prod;
			let find = false;
			if (prod) {
				prod.forEach(function (elem) {
					console.log(elem);
					let infos = elem.split('|');
					infos[1] = infos[1].toLowerCase();
					if (infos[1].indexOf(name) > -1 && !find) {
						find = true;
						return res.json({data: "ok", id: infos[0], where: infos[2], etage: infos[3]});
					}
				});
			}
			if (find)
				return;
			return res.json({data: "nok"});
		}
		else
			return res.json({data: "No user"});
	})

});

app.set('json spaces', 4);
app.listen(process.env.PORT || 8080, function () {
	console.log('Area server listening on port 8080');
});
