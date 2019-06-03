webpackJsonp([0],{

/***/ 165:
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncatched exception popping up in devtools
	return Promise.resolve().then(function() {
		throw new Error("Cannot find module '" + req + "'.");
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = 165;

/***/ }),

/***/ 209:
/***/ (function(module, exports, __webpack_require__) {

var map = {
	"../pages/add-prod/add-prod.module": [
		210
	],
	"../pages/home/home.module": [
		309
	],
	"../pages/param/param.module": [
		438
	],
	"../pages/search-prod/search-prod.module": [
		440
	]
};
function webpackAsyncContext(req) {
	var ids = map[req];
	if(!ids)
		return Promise.reject(new Error("Cannot find module '" + req + "'."));
	return Promise.all(ids.slice(1).map(__webpack_require__.e)).then(function() {
		return __webpack_require__(ids[0]);
	});
};
webpackAsyncContext.keys = function webpackAsyncContextKeys() {
	return Object.keys(map);
};
webpackAsyncContext.id = 209;
module.exports = webpackAsyncContext;

/***/ }),

/***/ 210:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AddProdPageModule", function() { return AddProdPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(27);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__add_prod__ = __webpack_require__(211);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var AddProdPageModule = /** @class */ (function () {
    function AddProdPageModule() {
    }
    AddProdPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["I" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__add_prod__["a" /* AddProdPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["d" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__add_prod__["a" /* AddProdPage */]),
            ],
        })
    ], AddProdPageModule);
    return AddProdPageModule;
}());

//# sourceMappingURL=add-prod.module.js.map

/***/ }),

/***/ 211:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AddProdPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(27);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_rxjs__ = __webpack_require__(212);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_rxjs___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_rxjs__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__ionic_native_nfc__ = __webpack_require__(132);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__angular_common_http__ = __webpack_require__(84);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__ionic_native_text_to_speech__ = __webpack_require__(85);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__ionic_storage__ = __webpack_require__(64);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};







/**
 * Generated class for the AddProdPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var AddProdPage = /** @class */ (function () {
    function AddProdPage(navCtrl, navParams, nfc, httpClient, tts, storage) {
        this.navCtrl = navCtrl;
        this.navParams = navParams;
        this.nfc = nfc;
        this.httpClient = httpClient;
        this.tts = tts;
        this.storage = storage;
        this.speed = 10;
        this.user = null;
        this.etage = null;
        this.name = null;
        this.tagId = "";
    }
    AddProdPage.prototype.ionViewDidEnter = function () {
        var _this = this;
        console.log("on active le nfc  not home");
        this.storage.get("ip").then(function (data) {
            _this.ip = data;
        });
        __WEBPACK_IMPORTED_MODULE_2_rxjs__["Observable"].fromEvent(window, 'beforeunload').subscribe(function (event) { return _this.tts.speak({ text: '' }); });
        this.nfc.enabled().then(function (resolve) {
            _this.addListenNFC2();
        }).catch(function (reject) {
            alert("NFC is not supported/activated by your Device");
        });
    };
    AddProdPage.prototype.ionViewDidLeave = function () {
        this.tts.speak({ text: '' });
        this.nfc.erase();
        this.listener.unsubscribe();
        console.log("on coupe le nfc");
    };
    AddProdPage.prototype.addListenNFC2 = function () {
        var _this = this;
        this.listener = this.nfc.addNdefListener().subscribe(function (data) {
            if (data && data.tag && data.tag.id) {
                var tagId = _this.nfc.bytesToHexString(data.tag.id);
                if (tagId) {
                    var payload = data.tag.ndefMessage[0].payload;
                    var tagContent = _this.nfc.bytesToString(payload).substring(3);
                    _this.tagId = tagId;
                    _this.scanned = true;
                    if (!_this.user || !_this.name || !_this.etage)
                        return;
                    var headers = new __WEBPACK_IMPORTED_MODULE_4__angular_common_http__["c" /* HttpHeaders */]().set('Content-Type', 'application/json');
                    var body = {
                        'user': _this.user,
                        'name': _this.name,
                        'etage': _this.etage,
                        'id': tagContent
                    };
                    var options = { headers: headers };
                    _this.product = _this.httpClient.post(_this.ip + '/user/add', body, options);
                    _this.product.subscribe(function (data) {
                        if (data.err)
                            alert("Hum hum");
                        else
                            alert(JSON.stringify(data));
                    });
                }
                else {
                    alert('NFC_NOT_DETECTED');
                }
            }
        });
    };
    AddProdPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({
            selector: 'page-add-prod',template:/*ion-inline-start:"/home/corentin/Public/Arlex_ProtoApp/src/pages/add-prod/add-prod.html"*/'<!--\n  Generated template for the AddProdPage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n-->\n<ion-header>\n  <ion-navbar>\n    <button menuToggle ion-button icon-only>\n      <ion-icon name="menu"></ion-icon>\n    </button>\n\n    <ion-title>Ajout Produits</ion-title>\n  </ion-navbar>\n</ion-header>\n\n<ion-content padding>\n  <ion-list>\n    <ion-item>\n      <ion-label>Nom de l\'utilisateur</ion-label>\n      <ion-input [(ngModel)]="user"></ion-input>\n    </ion-item>\n    <ion-item>\n      <ion-label>Nom armoire</ion-label>\n      <ion-input [(ngModel)]="name"></ion-input>\n    </ion-item>\n    <ion-item>\n      <ion-label>Etage</ion-label>\n      <ion-range min="1" max="3" step="1" pin="true" [(ngModel)]="etage">\n        <ion-icon small range-left name="remove"></ion-icon>\n        <ion-icon small range-right name="add"></ion-icon>\n      </ion-range>\n    </ion-item>\n  </ion-list>\n</ion-content>\n'/*ion-inline-end:"/home/corentin/Public/Arlex_ProtoApp/src/pages/add-prod/add-prod.html"*/,
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1_ionic_angular__["f" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_3__ionic_native_nfc__["a" /* NFC */],
            __WEBPACK_IMPORTED_MODULE_4__angular_common_http__["a" /* HttpClient */],
            __WEBPACK_IMPORTED_MODULE_5__ionic_native_text_to_speech__["a" /* TextToSpeech */],
            __WEBPACK_IMPORTED_MODULE_6__ionic_storage__["b" /* Storage */]])
    ], AddProdPage);
    return AddProdPage;
}());

//# sourceMappingURL=add-prod.js.map

/***/ }),

/***/ 309:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HomePageModule", function() { return HomePageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(27);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__home__ = __webpack_require__(310);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var HomePageModule = /** @class */ (function () {
    function HomePageModule() {
    }
    HomePageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["I" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__home__["a" /* HomePage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["d" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__home__["a" /* HomePage */]),
            ],
        })
    ], HomePageModule);
    return HomePageModule;
}());

//# sourceMappingURL=home.module.js.map

/***/ }),

/***/ 310:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return HomePage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(27);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__ionic_native_nfc__ = __webpack_require__(132);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_common_http__ = __webpack_require__(84);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_rxjs__ = __webpack_require__(212);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_rxjs___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4_rxjs__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__ionic_native_text_to_speech__ = __webpack_require__(85);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_moment__ = __webpack_require__(2);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_moment___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_6_moment__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__ionic_storage__ = __webpack_require__(64);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};








// plugins
var HomePage = /** @class */ (function () {
    function HomePage(navCtrl, navParams, nfc, httpClient, tts, storage) {
        this.navCtrl = navCtrl;
        this.navParams = navParams;
        this.nfc = nfc;
        this.httpClient = httpClient;
        this.tts = tts;
        this.storage = storage;
        this.speed = 10;
        this.tagId = "";
    }
    HomePage.prototype.ionViewDidEnter = function () {
        var _this = this;
        this.storage.get("ip").then(function (data) {
            _this.ip = data;
        });
        console.log("on active le nfc home");
        __WEBPACK_IMPORTED_MODULE_4_rxjs__["Observable"].fromEvent(window, 'beforeunload').subscribe(function (event) { return _this.tts.speak({ text: '' }); });
        this.nfc.enabled().then(function (resolve) {
            _this.addListenNFC();
        }).catch(function (reject) {
            alert("NFC is not supported/activated by your Device");
        });
    };
    HomePage.prototype.ionViewDidLeave = function () {
        this.tts.speak({ text: '' });
        this.nfc.erase();
        console.log("on coupe le nfc home");
        if (this.listener)
            this.listener.unsubscribe();
    };
    HomePage.prototype.addListenNFC = function () {
        var _this = this;
        this.listener = this.nfc.addNdefListener().subscribe(function (data) {
            if (data && data.tag && data.tag.id) {
                var tagId = _this.nfc.bytesToHexString(data.tag.id);
                if (tagId) {
                    var payload = data.tag.ndefMessage[0].payload;
                    var tagContent = _this.nfc.bytesToString(payload).substring(3);
                    _this.tagId = tagId;
                    _this.scanned = true;
                    // alert("tagid: "+ this.tagId + " | data : " + tagContent);
                    _this.product = _this.httpClient.get(_this.ip + '/infos/' + tagContent);
                    _this.product.subscribe(function (data) {
                        var aller = data.allergens.split(",");
                        var aller_unique = Array.from(new Set(aller));
                        data.allergens = aller_unique.join();
                        var months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
                        var date;
                        var dlc = data.dlc;
                        if (dlc.length === 5) {
                            date = __WEBPACK_IMPORTED_MODULE_6_moment___default()(data.dlc, "MM/YY").toDate();
                            var month = months[date.getMonth()];
                            var year = date.getFullYear();
                            data.dlc = "en " + month + " " + year;
                        }
                        else if (dlc.length == 8) {
                            date = __WEBPACK_IMPORTED_MODULE_6_moment___default()(data.dlc, "DD/MM/YY").toDate();
                            var day = date.getDate();
                            var month = months[date.getMonth()];
                            var year = date.getFullYear();
                            data.dlc = "le " + day + " " + month + " " + year;
                        }
                        else {
                            data.dlc = "pas";
                        }
                        var text = data.name + " périme " + data.dlc + ". Les allergènes qui le composent sont: " + data.allergens +
                            ". Il peut y avoir des traces éventuelles de : " + data.traces + ".";
                        _this.tts.speak({
                            text: text,
                            locale: 'fr-FR',
                            rate: _this.speed / 10
                        });
                        // alert('my data: '+ JSON.stringify(data));
                    });
                }
                else {
                    alert('NFC_NOT_DETECTED');
                }
            }
        });
    };
    HomePage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({
            selector: 'page-home',template:/*ion-inline-start:"/home/corentin/Public/Arlex_ProtoApp/src/pages/home/home.html"*/'<ion-header>\n  <ion-navbar>\n    <button menuToggle ion-button icon-only>\n      <ion-icon name="menu"></ion-icon>\n    </button>\n    <ion-title>\n      Arlex -  Informations\n    </ion-title>\n  </ion-navbar>\n</ion-header>\n\n<ion-content padding>\n  <p>\n    Veuillez approcher un produit.\n  </p>\n  Vitesse du TTS:\n  <ion-item>\n    <ion-range [(ngModel)]="speed" color="danger" min="1" max="30" step=1 pin="true">\n      <ion-label range-left>0.1</ion-label>\n      <ion-label range-right>3</ion-label>\n    </ion-range>\n  </ion-item>\n\n</ion-content>\n'/*ion-inline-end:"/home/corentin/Public/Arlex_ProtoApp/src/pages/home/home.html"*/
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1_ionic_angular__["f" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_2__ionic_native_nfc__["a" /* NFC */],
            __WEBPACK_IMPORTED_MODULE_3__angular_common_http__["a" /* HttpClient */],
            __WEBPACK_IMPORTED_MODULE_5__ionic_native_text_to_speech__["a" /* TextToSpeech */],
            __WEBPACK_IMPORTED_MODULE_7__ionic_storage__["b" /* Storage */]])
    ], HomePage);
    return HomePage;
}());

//# sourceMappingURL=home.js.map

/***/ }),

/***/ 438:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ParamPageModule", function() { return ParamPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(27);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__param__ = __webpack_require__(439);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var ParamPageModule = /** @class */ (function () {
    function ParamPageModule() {
    }
    ParamPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["I" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__param__["a" /* ParamPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["d" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__param__["a" /* ParamPage */]),
            ],
        })
    ], ParamPageModule);
    return ParamPageModule;
}());

//# sourceMappingURL=param.module.js.map

/***/ }),

/***/ 439:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ParamPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(27);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__ionic_storage__ = __webpack_require__(64);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



/**
 * Generated class for the ParamPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var ParamPage = /** @class */ (function () {
    function ParamPage(navCtrl, navParams, storage) {
        this.navCtrl = navCtrl;
        this.navParams = navParams;
        this.storage = storage;
        this.ip = "https://api-proto-arlex.herokuapp.com";
    }
    ParamPage.prototype.ionViewDidLoad = function () {
        var _this = this;
        console.log('ionViewDidLoad ParamPage');
        this.storage.get("ip").then(function (data) {
            if (data)
                _this.ip = data;
        });
    };
    ParamPage.prototype.save = function () {
        console.log("lol:", this.ip);
        if (this.ip) {
            if (this.ip.startsWith("http://") || this.ip.startsWith("https://"))
                this.storage.set("ip", this.ip);
            else {
                this.ip = "http://" + this.ip;
                console.log(this.ip);
                this.storage.set("ip", this.ip);
            }
        }
    };
    ParamPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({
            selector: 'page-param',template:/*ion-inline-start:"/home/corentin/Public/Arlex_ProtoApp/src/pages/param/param.html"*/'<!--\n  Generated template for the ParamPage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n-->\n<ion-header>\n  <ion-navbar>\n    <button menuToggle ion-button icon-only>\n      <ion-icon name="menu"></ion-icon>\n    </button>\n    <ion-title>\n      Arlex -  Params\n    </ion-title>\n    <ion-buttons end>\n      <button ion-button icon-only (click)="ip = \'https://api-proto-arlex.herokuapp.com\'; save()">\n        <ion-icon name="refresh"></ion-icon>\n      </button>\n    </ion-buttons>\n  </ion-navbar>\n</ion-header>\n\n<ion-content padding>\n  <ion-list>\n    <ion-item>\n      <ion-label>Ip de l\'api</ion-label>\n      <ion-input [(ngModel)]="ip" [value]="ip"></ion-input>\n    </ion-item>\n    <button ion-button full (click)="save()">SAuvegarder</button>\n  </ion-list>\n\n</ion-content>\n'/*ion-inline-end:"/home/corentin/Public/Arlex_ProtoApp/src/pages/param/param.html"*/,
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1_ionic_angular__["f" /* NavController */], __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* NavParams */], __WEBPACK_IMPORTED_MODULE_2__ionic_storage__["b" /* Storage */]])
    ], ParamPage);
    return ParamPage;
}());

//# sourceMappingURL=param.js.map

/***/ }),

/***/ 440:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SearchProdPageModule", function() { return SearchProdPageModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(27);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__search_prod__ = __webpack_require__(441);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var SearchProdPageModule = /** @class */ (function () {
    function SearchProdPageModule() {
    }
    SearchProdPageModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["I" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__search_prod__["a" /* SearchProdPage */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["d" /* IonicPageModule */].forChild(__WEBPACK_IMPORTED_MODULE_2__search_prod__["a" /* SearchProdPage */]),
            ],
        })
    ], SearchProdPageModule);
    return SearchProdPageModule;
}());

//# sourceMappingURL=search-prod.module.js.map

/***/ }),

/***/ 441:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return SearchProdPage; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(27);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_common_http__ = __webpack_require__(84);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__ionic_native_text_to_speech__ = __webpack_require__(85);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__ionic_storage__ = __webpack_require__(64);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_moment__ = __webpack_require__(2);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_moment___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_5_moment__);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};






/**
 * Generated class for the SearchProdPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
var SearchProdPage = /** @class */ (function () {
    function SearchProdPage(navCtrl, navParams, httpClient, tts, storage) {
        this.navCtrl = navCtrl;
        this.navParams = navParams;
        this.httpClient = httpClient;
        this.tts = tts;
        this.storage = storage;
        this.user = null;
        this.name = null;
        this.info = null;
    }
    SearchProdPage.prototype.ionViewDidLoad = function () {
        var _this = this;
        console.log('ionViewDidLoad SearchProdPage');
        this.storage.get("ip").then(function (data) {
            _this.ip = data;
        });
    };
    SearchProdPage.prototype.searchProd = function () {
        var _this = this;
        if (!this.user || !this.name)
            return;
        var headers = new __WEBPACK_IMPORTED_MODULE_2__angular_common_http__["c" /* HttpHeaders */]().set('Content-Type', 'application/json');
        var body = {
            'user': this.user,
            'prod': this.name,
        };
        var options = { headers: headers };
        this.product = this.httpClient.post(this.ip + '/user/search', body, options);
        this.product.subscribe(function (data) {
            console.log("infos == ", _this.info);
            if (data.err)
                alert("Hum hum");
            else if (data.data == "ok") {
                var infos_1 = data;
                if (_this.info == true) {
                    _this.product = _this.httpClient.get(_this.ip + '/infos/' + data.id);
                    _this.product.subscribe(function (data) {
                        var aller = data.allergens.split(",");
                        var aller_unique = Array.from(new Set(aller));
                        data.allergens = aller_unique.join();
                        var months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
                        var date;
                        var dlc = data.dlc;
                        if (dlc.length === 5) {
                            date = __WEBPACK_IMPORTED_MODULE_5_moment___default()(data.dlc, "MM/YY").toDate();
                            var month = months[date.getMonth()];
                            var year = date.getFullYear();
                            data.dlc = "en " + month + " " + year;
                        }
                        else if (dlc.length == 8) {
                            date = __WEBPACK_IMPORTED_MODULE_5_moment___default()(data.dlc, "DD/MM/YY").toDate();
                            var day = date.getDate();
                            var month = months[date.getMonth()];
                            var year = date.getFullYear();
                            data.dlc = "le " + day + " " + month + " " + year;
                        }
                        else
                            data.dlc = "pas";
                        var text_inf = data.name + " périme " + data.dlc + ". Les allergènes qui le composent sont: " + data.allergens +
                            ". Il peut y avoir des traces éventuelles de : " + data.traces + ".";
                        var text = _this.name + " se trouve dans le placard " + infos_1.where + " à l'étage numéro " + infos_1.etage + ". " + text_inf;
                        _this.tts.speak({
                            text: text,
                            locale: 'fr-FR',
                        });
                    });
                }
                else {
                    var text = _this.name + " se trouve dans le placard " + infos_1.where + " à l'étage numéro " + infos_1.etage + ".";
                    _this.tts.speak({
                        text: text,
                        locale: 'fr-FR',
                    });
                }
            }
            else {
                var text = "Produit non trouvé.";
                _this.tts.speak({
                    text: text,
                    locale: 'fr-FR',
                });
            }
        });
    };
    SearchProdPage = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({
            selector: 'page-search-prod',template:/*ion-inline-start:"/home/corentin/Public/Arlex_ProtoApp/src/pages/search-prod/search-prod.html"*/'<!--\n  Generated template for the SearchProdPage page.\n\n  See http://ionicframework.com/docs/components/#navigation for more info on\n  Ionic pages and navigation.\n-->\n<ion-header>\n  <ion-navbar>\n    <button menuToggle ion-button icon-only>\n      <ion-icon name="menu"></ion-icon>\n    </button>\n    <ion-title>Recherche Produit (Assistant)</ion-title>\n  </ion-navbar>\n</ion-header>\n\n<ion-content padding>\n  <ion-list>\n    <ion-item>\n      <ion-label>Nom de l\'utilisateur</ion-label>\n      <ion-input [(ngModel)]="user"></ion-input>\n    </ion-item>\n    <ion-item>\n      <ion-label>Nom produit</ion-label>\n      <ion-input [(ngModel)]="name"></ion-input>\n    </ion-item>\n    <ion-item>\n      <ion-label>Informations sur le produit</ion-label>\n      <ion-checkbox [(ngModel)]="info"></ion-checkbox>\n    </ion-item>\n    <button ion-button full (click)="searchProd()">Rechercher</button>\n  </ion-list>\n</ion-content>\n'/*ion-inline-end:"/home/corentin/Public/Arlex_ProtoApp/src/pages/search-prod/search-prod.html"*/,
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1_ionic_angular__["f" /* NavController */],
            __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["g" /* NavParams */],
            __WEBPACK_IMPORTED_MODULE_2__angular_common_http__["a" /* HttpClient */],
            __WEBPACK_IMPORTED_MODULE_3__ionic_native_text_to_speech__["a" /* TextToSpeech */],
            __WEBPACK_IMPORTED_MODULE_4__ionic_storage__["b" /* Storage */]])
    ], SearchProdPage);
    return SearchProdPage;
}());

//# sourceMappingURL=search-prod.js.map

/***/ }),

/***/ 483:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser_dynamic__ = __webpack_require__(484);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__app_module__ = __webpack_require__(488);


Object(__WEBPACK_IMPORTED_MODULE_0__angular_platform_browser_dynamic__["a" /* platformBrowserDynamic */])().bootstrapModule(__WEBPACK_IMPORTED_MODULE_1__app_module__["a" /* AppModule */]);
//# sourceMappingURL=main.js.map

/***/ }),

/***/ 488:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__ = __webpack_require__(43);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_ionic_angular__ = __webpack_require__(27);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__ = __webpack_require__(481);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__ionic_native_status_bar__ = __webpack_require__(482);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__app_component__ = __webpack_require__(813);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__ionic_native_nfc__ = __webpack_require__(132);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__angular_common_http__ = __webpack_require__(84);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8__ionic_native_text_to_speech__ = __webpack_require__(85);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9__pages_add_prod_add_prod_module__ = __webpack_require__(210);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_10__pages_search_prod_search_prod_module__ = __webpack_require__(440);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_11__pages_home_home_module__ = __webpack_require__(309);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_12__ionic_storage__ = __webpack_require__(64);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_13__pages_param_param_module__ = __webpack_require__(438);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};














var AppModule = /** @class */ (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["I" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_5__app_component__["a" /* MyApp */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__["a" /* BrowserModule */],
                __WEBPACK_IMPORTED_MODULE_7__angular_common_http__["b" /* HttpClientModule */],
                __WEBPACK_IMPORTED_MODULE_11__pages_home_home_module__["HomePageModule"],
                __WEBPACK_IMPORTED_MODULE_9__pages_add_prod_add_prod_module__["AddProdPageModule"],
                __WEBPACK_IMPORTED_MODULE_13__pages_param_param_module__["ParamPageModule"],
                __WEBPACK_IMPORTED_MODULE_10__pages_search_prod_search_prod_module__["SearchProdPageModule"],
                __WEBPACK_IMPORTED_MODULE_12__ionic_storage__["a" /* IonicStorageModule */].forRoot(),
                __WEBPACK_IMPORTED_MODULE_2_ionic_angular__["c" /* IonicModule */].forRoot(__WEBPACK_IMPORTED_MODULE_5__app_component__["a" /* MyApp */], {}, {
                    links: [
                        { loadChildren: '../pages/add-prod/add-prod.module#AddProdPageModule', name: 'AddProdPage', segment: 'add-prod', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/home/home.module#HomePageModule', name: 'HomePage', segment: 'home', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/param/param.module#ParamPageModule', name: 'ParamPage', segment: 'param', priority: 'low', defaultHistory: [] },
                        { loadChildren: '../pages/search-prod/search-prod.module#SearchProdPageModule', name: 'SearchProdPage', segment: 'search-prod', priority: 'low', defaultHistory: [] }
                    ]
                })
            ],
            bootstrap: [__WEBPACK_IMPORTED_MODULE_2_ionic_angular__["a" /* IonicApp */]],
            entryComponents: [
                __WEBPACK_IMPORTED_MODULE_5__app_component__["a" /* MyApp */],
            ],
            providers: [
                __WEBPACK_IMPORTED_MODULE_4__ionic_native_status_bar__["a" /* StatusBar */],
                __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__["a" /* SplashScreen */],
                __WEBPACK_IMPORTED_MODULE_6__ionic_native_nfc__["a" /* NFC */],
                __WEBPACK_IMPORTED_MODULE_6__ionic_native_nfc__["b" /* Ndef */],
                __WEBPACK_IMPORTED_MODULE_8__ionic_native_text_to_speech__["a" /* TextToSpeech */],
                { provide: __WEBPACK_IMPORTED_MODULE_1__angular_core__["u" /* ErrorHandler */], useClass: __WEBPACK_IMPORTED_MODULE_2_ionic_angular__["b" /* IonicErrorHandler */] }
            ]
        })
    ], AppModule);
    return AppModule;
}());

//# sourceMappingURL=app.module.js.map

/***/ }),

/***/ 795:
/***/ (function(module, exports, __webpack_require__) {

var map = {
	"./af": 311,
	"./af.js": 311,
	"./ar": 312,
	"./ar-dz": 313,
	"./ar-dz.js": 313,
	"./ar-kw": 314,
	"./ar-kw.js": 314,
	"./ar-ly": 315,
	"./ar-ly.js": 315,
	"./ar-ma": 316,
	"./ar-ma.js": 316,
	"./ar-sa": 317,
	"./ar-sa.js": 317,
	"./ar-tn": 318,
	"./ar-tn.js": 318,
	"./ar.js": 312,
	"./az": 319,
	"./az.js": 319,
	"./be": 320,
	"./be.js": 320,
	"./bg": 321,
	"./bg.js": 321,
	"./bm": 322,
	"./bm.js": 322,
	"./bn": 323,
	"./bn.js": 323,
	"./bo": 324,
	"./bo.js": 324,
	"./br": 325,
	"./br.js": 325,
	"./bs": 326,
	"./bs.js": 326,
	"./ca": 327,
	"./ca.js": 327,
	"./cs": 328,
	"./cs.js": 328,
	"./cv": 329,
	"./cv.js": 329,
	"./cy": 330,
	"./cy.js": 330,
	"./da": 331,
	"./da.js": 331,
	"./de": 332,
	"./de-at": 333,
	"./de-at.js": 333,
	"./de-ch": 334,
	"./de-ch.js": 334,
	"./de.js": 332,
	"./dv": 335,
	"./dv.js": 335,
	"./el": 336,
	"./el.js": 336,
	"./en-SG": 337,
	"./en-SG.js": 337,
	"./en-au": 338,
	"./en-au.js": 338,
	"./en-ca": 339,
	"./en-ca.js": 339,
	"./en-gb": 340,
	"./en-gb.js": 340,
	"./en-ie": 341,
	"./en-ie.js": 341,
	"./en-il": 342,
	"./en-il.js": 342,
	"./en-nz": 343,
	"./en-nz.js": 343,
	"./eo": 344,
	"./eo.js": 344,
	"./es": 345,
	"./es-do": 346,
	"./es-do.js": 346,
	"./es-us": 347,
	"./es-us.js": 347,
	"./es.js": 345,
	"./et": 348,
	"./et.js": 348,
	"./eu": 349,
	"./eu.js": 349,
	"./fa": 350,
	"./fa.js": 350,
	"./fi": 351,
	"./fi.js": 351,
	"./fo": 352,
	"./fo.js": 352,
	"./fr": 353,
	"./fr-ca": 354,
	"./fr-ca.js": 354,
	"./fr-ch": 355,
	"./fr-ch.js": 355,
	"./fr.js": 353,
	"./fy": 356,
	"./fy.js": 356,
	"./ga": 357,
	"./ga.js": 357,
	"./gd": 358,
	"./gd.js": 358,
	"./gl": 359,
	"./gl.js": 359,
	"./gom-latn": 360,
	"./gom-latn.js": 360,
	"./gu": 361,
	"./gu.js": 361,
	"./he": 362,
	"./he.js": 362,
	"./hi": 363,
	"./hi.js": 363,
	"./hr": 364,
	"./hr.js": 364,
	"./hu": 365,
	"./hu.js": 365,
	"./hy-am": 366,
	"./hy-am.js": 366,
	"./id": 367,
	"./id.js": 367,
	"./is": 368,
	"./is.js": 368,
	"./it": 369,
	"./it-ch": 370,
	"./it-ch.js": 370,
	"./it.js": 369,
	"./ja": 371,
	"./ja.js": 371,
	"./jv": 372,
	"./jv.js": 372,
	"./ka": 373,
	"./ka.js": 373,
	"./kk": 374,
	"./kk.js": 374,
	"./km": 375,
	"./km.js": 375,
	"./kn": 376,
	"./kn.js": 376,
	"./ko": 377,
	"./ko.js": 377,
	"./ku": 378,
	"./ku.js": 378,
	"./ky": 379,
	"./ky.js": 379,
	"./lb": 380,
	"./lb.js": 380,
	"./lo": 381,
	"./lo.js": 381,
	"./lt": 382,
	"./lt.js": 382,
	"./lv": 383,
	"./lv.js": 383,
	"./me": 384,
	"./me.js": 384,
	"./mi": 385,
	"./mi.js": 385,
	"./mk": 386,
	"./mk.js": 386,
	"./ml": 387,
	"./ml.js": 387,
	"./mn": 388,
	"./mn.js": 388,
	"./mr": 389,
	"./mr.js": 389,
	"./ms": 390,
	"./ms-my": 391,
	"./ms-my.js": 391,
	"./ms.js": 390,
	"./mt": 392,
	"./mt.js": 392,
	"./my": 393,
	"./my.js": 393,
	"./nb": 394,
	"./nb.js": 394,
	"./ne": 395,
	"./ne.js": 395,
	"./nl": 396,
	"./nl-be": 397,
	"./nl-be.js": 397,
	"./nl.js": 396,
	"./nn": 398,
	"./nn.js": 398,
	"./pa-in": 399,
	"./pa-in.js": 399,
	"./pl": 400,
	"./pl.js": 400,
	"./pt": 401,
	"./pt-br": 402,
	"./pt-br.js": 402,
	"./pt.js": 401,
	"./ro": 403,
	"./ro.js": 403,
	"./ru": 404,
	"./ru.js": 404,
	"./sd": 405,
	"./sd.js": 405,
	"./se": 406,
	"./se.js": 406,
	"./si": 407,
	"./si.js": 407,
	"./sk": 408,
	"./sk.js": 408,
	"./sl": 409,
	"./sl.js": 409,
	"./sq": 410,
	"./sq.js": 410,
	"./sr": 411,
	"./sr-cyrl": 412,
	"./sr-cyrl.js": 412,
	"./sr.js": 411,
	"./ss": 413,
	"./ss.js": 413,
	"./sv": 414,
	"./sv.js": 414,
	"./sw": 415,
	"./sw.js": 415,
	"./ta": 416,
	"./ta.js": 416,
	"./te": 417,
	"./te.js": 417,
	"./tet": 418,
	"./tet.js": 418,
	"./tg": 419,
	"./tg.js": 419,
	"./th": 420,
	"./th.js": 420,
	"./tl-ph": 421,
	"./tl-ph.js": 421,
	"./tlh": 422,
	"./tlh.js": 422,
	"./tr": 423,
	"./tr.js": 423,
	"./tzl": 424,
	"./tzl.js": 424,
	"./tzm": 425,
	"./tzm-latn": 426,
	"./tzm-latn.js": 426,
	"./tzm.js": 425,
	"./ug-cn": 427,
	"./ug-cn.js": 427,
	"./uk": 428,
	"./uk.js": 428,
	"./ur": 429,
	"./ur.js": 429,
	"./uz": 430,
	"./uz-latn": 431,
	"./uz-latn.js": 431,
	"./uz.js": 430,
	"./vi": 432,
	"./vi.js": 432,
	"./x-pseudo": 433,
	"./x-pseudo.js": 433,
	"./yo": 434,
	"./yo.js": 434,
	"./zh-cn": 435,
	"./zh-cn.js": 435,
	"./zh-hk": 436,
	"./zh-hk.js": 436,
	"./zh-tw": 437,
	"./zh-tw.js": 437
};
function webpackContext(req) {
	return __webpack_require__(webpackContextResolve(req));
};
function webpackContextResolve(req) {
	var id = map[req];
	if(!(id + 1)) // check for number or string
		throw new Error("Cannot find module '" + req + "'.");
	return id;
};
webpackContext.keys = function webpackContextKeys() {
	return Object.keys(map);
};
webpackContext.resolve = webpackContextResolve;
module.exports = webpackContext;
webpackContext.id = 795;

/***/ }),

/***/ 813:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return MyApp; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ionic_angular__ = __webpack_require__(27);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__ionic_native_status_bar__ = __webpack_require__(482);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__ = __webpack_require__(481);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__pages_home_home__ = __webpack_require__(310);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__pages_add_prod_add_prod__ = __webpack_require__(211);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__pages_search_prod_search_prod__ = __webpack_require__(441);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__pages_param_param__ = __webpack_require__(439);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};








var MyApp = /** @class */ (function () {
    function MyApp(platform, statusBar, splashScreen) {
        this.platform = platform;
        this.statusBar = statusBar;
        this.splashScreen = splashScreen;
        this.rootPage = __WEBPACK_IMPORTED_MODULE_7__pages_param_param__["a" /* ParamPage */];
        // used for an example of ngFor and navigation
        this.initializeApp();
        this.pages = [
            { title: 'Accueil', component: __WEBPACK_IMPORTED_MODULE_4__pages_home_home__["a" /* HomePage */] },
            { title: 'Ajout produits', component: __WEBPACK_IMPORTED_MODULE_5__pages_add_prod_add_prod__["a" /* AddProdPage */] },
            { title: 'Recherche produit (Assistant)', component: __WEBPACK_IMPORTED_MODULE_6__pages_search_prod_search_prod__["a" /* SearchProdPage */] },
            { title: 'Params', component: __WEBPACK_IMPORTED_MODULE_7__pages_param_param__["a" /* ParamPage */] }
        ];
    }
    MyApp.prototype.initializeApp = function () {
        var _this = this;
        this.platform.ready().then(function () {
            // Okay, so the platform is ready and our plugins are available.
            // Here you can do any higher level native things you might need.
            _this.statusBar.styleDefault();
            _this.splashScreen.hide();
        });
    };
    MyApp.prototype.openPage = function (page) {
        // Reset the content nav to have just this page
        // we wouldn't want the back button to show in this scenario
        this.nav.setRoot(page.component);
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_8" /* ViewChild */])(__WEBPACK_IMPORTED_MODULE_1_ionic_angular__["e" /* Nav */]),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_1_ionic_angular__["e" /* Nav */])
    ], MyApp.prototype, "nav", void 0);
    MyApp = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({template:/*ion-inline-start:"/home/corentin/Public/Arlex_ProtoApp/src/app/app.html"*/'<ion-menu [content]="content">\n<ion-header>\n  <ion-toolbar>\n    <ion-title>Menu</ion-title>\n  </ion-toolbar>\n</ion-header>\n\n<ion-content>\n  <ion-list>\n    <button menuClose ion-item *ngFor="let p of pages" (click)="openPage(p)">\n      {{p.title}}\n    </button>\n  </ion-list>\n</ion-content>\n\n</ion-menu>\n\n<!-- Disable swipe-to-go-back because it\'s poor UX to combine STGB with side menus -->\n<ion-nav [root]="rootPage" #content swipeBackEnabled="false"></ion-nav>\n'/*ion-inline-end:"/home/corentin/Public/Arlex_ProtoApp/src/app/app.html"*/
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1_ionic_angular__["h" /* Platform */], __WEBPACK_IMPORTED_MODULE_2__ionic_native_status_bar__["a" /* StatusBar */], __WEBPACK_IMPORTED_MODULE_3__ionic_native_splash_screen__["a" /* SplashScreen */]])
    ], MyApp);
    return MyApp;
}());

//# sourceMappingURL=app.component.js.map

/***/ })

},[483]);
//# sourceMappingURL=main.js.map