import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {Observable} from "rxjs";
import {NFC} from "@ionic-native/nfc";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {TextToSpeech} from "@ionic-native/text-to-speech";
import Moment from "moment";
import {Storage} from "@ionic/storage";

/**
 * Generated class for the AddProdPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-add-prod',
  templateUrl: 'add-prod.html',
})
export class AddProdPage {

  granted: boolean;
  scanned: boolean;
  tagId: string;
  product: Observable<any>;
  speed = 10;
  user = null;
  etage = null;
  name = null;
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
    console.log("on active le nfc  not home");
    this.storage.get("ip").then(data => {
      this.ip = data;
    });
    Observable.fromEvent(window, 'beforeunload').subscribe(event => this.tts.speak({text: ''}));
    this.nfc.enabled().then((resolve) => {
      this.addListenNFC2();
    }).catch((reject) => {
      alert("NFC is not supported/activated by your Device");
    });
  }

  ionViewDidLeave() {
    this.tts.speak({text: ''});
    this.nfc.erase();
    this.listener.unsubscribe();
    console.log("on coupe le nfc");
  }


  addListenNFC2() {
    this.listener = this.nfc.addNdefListener().subscribe(data => {
      if (data && data.tag && data.tag.id) {
        let tagId = this.nfc.bytesToHexString(data.tag.id);
        if (tagId) {
          let payload = data.tag. ndefMessage[0].payload;
          let tagContent = this.nfc.bytesToString(payload).substring(3);
          this.tagId = tagId;
          this.scanned = true;

          if (!this.user || !this.name || !this.etage)
            return;
          const headers = new HttpHeaders().set('Content-Type', 'application/json');
          let body = {
            'user': this.user,
            'name': this.name,
            'etage': this.etage,
            'id': tagContent
          };
          let options = { headers: headers };
          this.product = this.httpClient.post(this.ip + '/user/add', body, options);
          this.product.subscribe(data => {
            if (data.err)
              alert("Hum hum");
            else
              alert(JSON.stringify(data));
          });
        } else {
          alert('NFC_NOT_DETECTED');
        }
      }
    });
  }
}
