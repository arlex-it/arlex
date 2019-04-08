import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {Storage} from "@ionic/storage";

/**
 * Generated class for the ParamPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-param',
  templateUrl: 'param.html',
})
export class ParamPage {

  ip = "https://api-proto-arlex.herokuapp.com";

  constructor(public navCtrl: NavController, public navParams: NavParams, private storage: Storage) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ParamPage');
    this.storage.get("ip").then(data=> {
      if (data)
        this.ip = data;
    })
  }

  save() {
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
  }

}
