import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ParamPage } from './param';

@NgModule({
  declarations: [
    ParamPage,
  ],
  imports: [
    IonicPageModule.forChild(ParamPage),
  ],
})
export class ParamPageModule {}
