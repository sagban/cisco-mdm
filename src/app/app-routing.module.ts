import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {HomeComponent} from './home/home.component';
import {LoginHomeComponent} from './login-home/login-home.component';

const routes: Routes = [
  { path : '', component: HomeComponent},
  { path : 'login', component: LoginHomeComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
