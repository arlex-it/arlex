import {Component, ViewChild} from '@angular/core';
import { Nav, Platform } from 'ionic-angular';
import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';

import { HomePage } from '../pages/home/home';
import {AddProdPage} from "../pages/add-prod/add-prod";
import {SearchProdPage} from "../pages/search-prod/search-prod";
import {ParamPage} from "../pages/param/param";
@Component({
  templateUrl: 'app.html'
})
export class MyApp {
  @ViewChild(Nav) nav: Nav;

  rootPage: any = ParamPage;

  pages: Array<{title: string, component: any}>;

  constructor(public platform: Platform, public statusBar: StatusBar, public splashScreen: SplashScreen) {
    // used for an example of ngFor and navigation
    this.initializeApp();

    this.pages = [
      {title: 'Accueil', component: HomePage},
      {title: 'Ajout produits', component: AddProdPage},
      {title: 'Recherche produit (Assistant)', component: SearchProdPage},
      {title: 'Params', component: ParamPage}
      ];
  }
  initializeApp() {
    this.platform.ready().then(() => {
      // Okay, so the platform is ready and our plugins are available.
      // Here you can do any higher level native things you might need.
      this.statusBar.styleDefault();
      this.splashScreen.hide();
    });
  }

  openPage(page) {
    // Reset the content nav to have just this page
    // we wouldn't want the back button to show in this scenario
    this.nav.setRoot(page.component);
  }
}

