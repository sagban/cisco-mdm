import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {HomeComponent} from './home/home.component';
import {LoginHomeComponent} from './login-home/login-home.component';

import {DashboardAdminComponent} from './dashboard-admin/dashboard-admin.component';
import {AuthGuard} from "./_guard/auth.guard";


const routes: Routes = [
  { path : '', component: HomeComponent},
  { path : 'login', component: LoginHomeComponent},
  { path : 'dashboard/admin', component: DashboardAdminComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
