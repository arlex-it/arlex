import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {NFC} from "@ionic-native/nfc";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {TextToSpeech} from "@ionic-native/text-to-speech";
import Moment from 'moment';
import {Storage} from "@ionic/storage";

// plugins

@IonicPage()
@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  granted: boolean;
  denied: boolean;
  scanned: boolean;
  tagId: string;
  product: Observable<any>;
  speed = 10;
  listener;
  ip;

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private nfc: NFC,
    public httpClient: HttpClient,
    private tts: TextToSpeech,
    private storage: Storage) {

    this.tagId = "";
  }

  ionViewDidEnter() {
    this.storage.get("ip").then(data => {
      this.ip = data;
    });
    console.log("on active le nfc home");
    Observable.fromEvent(window, 'beforeunload').subscribe(event => this.tts.speak({text: ''}));
    this.nfc.enabled().then((resolve) => {
      this.addListenNFC();
    }).catch((reject) => {
      alert("NFC is not supported/activated by your Device");
    });
  }

  ionViewDidLeave() {
    this.tts.speak({text: ''});
    this.nfc.erase();
    console.log("on coupe le nfc home");
    if (this.listener)
      this.listener.unsubscribe();
  }


  addListenNFC() {
    this.listener = this.nfc.addNdefListener().subscribe(data => {
      if (data && data.tag && data.tag.id) {
        let tagId = this.nfc.bytesToHexString(data.tag.id);
        if (tagId) {
          let payload = data.tag. ndefMessage[0].payload;
          let tagContent = this.nfc.bytesToString(payload).substring(3);
          this.tagId = tagId;
          this.scanned = true;

          // alert("tagid: "+ this.tagId + " | data : " + tagContent);
          this.product = this.httpClient.get(this.ip + '/infos/' + tagContent);
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
            } else {
              data.dlc = "pas";
            }
            let text = data.name + " périme " + data.dlc + ". Les allergènes qui le composent sont: " + data.allergens +
              ". Il peut y avoir des traces éventuelles de : " + data.traces + ".";
            this.tts.speak({
              text: text,
              locale: 'fr-FR',
              rate: this.speed / 10
            });
            // alert('my data: '+ JSON.stringify(data));
          })

        } else {
          alert('NFC_NOT_DETECTED');
        }
      }
    });
  }

}

