import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {TextToSpeech} from "@ionic-native/text-to-speech";
import {Storage} from "@ionic/storage";
import Moment from "moment";

/**
 * Generated class for the SearchProdPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-search-prod',
  templateUrl: 'search-prod.html',
})
export class SearchProdPage {
  user = null;
  name = null;
  product: Observable<any>;
  ip;
  info = null;
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public httpClient: HttpClient,
              private tts: TextToSpeech,
              private storage: Storage) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad SearchProdPage');
    this.storage.get("ip").then(data => {
      this.ip = data;
    });

  }

  searchProd() {
    if (!this.user || !this.name)
      return;
    const headers = new HttpHeaders().set('Content-Type', 'application/json');
    let body = {
      'user': this.user,
      'prod': this.name,
    };
    let options = { headers: headers };

    this.product = this.httpClient.post(this.ip + '/user/search', body, options);
    this.product.subscribe(data => {
      console.log("infos == ", this.info);
      if (data.err)
        alert("Hum hum");
      else if (data.data == "ok") {
        let infos = data;
        if (this.info == true) {
          this.product = this.httpClient.get(this.ip + '/infos/' + data.id);
          this.product.subscribe(data => {
            let aller = data.allergens.split(",");
            let aller_unique = Array.from(new Set(aller));
            data.allergens = aller_unique.join();
            let months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
            let date;
            let dlc = data.dlc;
            if (dlc.length === 5) {
              date = Moment(data.dlc, "MM/YY").toDate();
              let month = months[date.getMonth()];
              let year = date.getFullYear();
              data.dlc = "en " + month + " " + year;
            } else if (dlc.length == 8) {
              date = Moment(data.dlc, "DD/MM/YY").toDate();
              let day = date.getDate();
              let month = months[date.getMonth()];
              let year = date.getFullYear();
              data.dlc = "le " + day + " " + month + " " + year;
            } else
              data.dlc = "pas";
            let text_inf = data.name + " périme " + data.dlc + ". Les allergènes qui le composent sont: " + data.allergens +
              ". Il peut y avoir des traces éventuelles de : " + data.traces + ".";

            let text = this.name + " se trouve dans le placard " + infos.where + " à l'étage numéro " + infos.etage + ". " + text_inf;
            this.tts.speak({
              text: text,
              locale: 'fr-FR',
            });
          });
        } else {
          let text = this.name + " se trouve dans le placard " + infos.where + " à l'étage numéro " + infos.etage + ".";
          this.tts.speak({
            text: text,
            locale: 'fr-FR',
          });
        }
      } else {
        let text = "Produit non trouvé.";
        this.tts.speak({
          text: text,
          locale: 'fr-FR',
        });
      }
    });

  }
}
