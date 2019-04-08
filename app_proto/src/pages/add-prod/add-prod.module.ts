import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AddProdPage } from './add-prod';

@NgModule({
  declarations: [
    AddProdPage,
  ],
  imports: [
    IonicPageModule.forChild(AddProdPage),
  ],
})
export class AddProdPageModule {}
