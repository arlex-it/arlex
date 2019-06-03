import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import { IonicApp, IonicErrorHandler, IonicModule } from 'ionic-angular';
import { SplashScreen } from '@ionic-native/splash-screen';
import { StatusBar } from '@ionic-native/status-bar';

import { MyApp } from './app.component';
import { HomePage } from '../pages/home/home';
import {Ndef, NFC} from "@ionic-native/nfc";
import { HttpClientModule } from '@angular/common/http';
import {TextToSpeech} from "@ionic-native/text-to-speech";
import {AddProdPageModule} from "../pages/add-prod/add-prod.module";
import {SearchProdPageModule} from "../pages/search-prod/search-prod.module";
import {HomePageModule} from "../pages/home/home.module";
import {IonicStorageModule} from "@ionic/storage";
import {ParamPageModule} from "../pages/param/param.module";

@NgModule({
  declarations: [
    MyApp,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    HomePageModule,
    AddProdPageModule,
    ParamPageModule,
    SearchProdPageModule,
    IonicStorageModule.forRoot(),
    IonicModule.forRoot(MyApp)
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
  ],
  providers: [
    StatusBar,
    SplashScreen,
    NFC,
    Ndef,
    TextToSpeech,
    {provide: ErrorHandler, useClass: IonicErrorHandler}
  ]
})
export class AppModule {}
