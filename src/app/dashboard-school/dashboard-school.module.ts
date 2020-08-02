import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardSchoolRoutingModule } from "./dashboard-school-routing.module";
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { HomeComponent } from './home/home.component';
import { GrievanceComponent } from './grievance/grievance.component';
import { CameraComponent } from './camera/camera.component';
import { ReportCardComponent } from './report-card/report-card.component';
import { ReportsComponent } from './reports/reports.component';


@NgModule({
  declarations: [
  HomeComponent,
  GrievanceComponent,
  CameraComponent,
  ReportCardComponent,
  ReportsComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    DashboardSchoolRoutingModule
  ]
})
export class DashboardSchoolModule { }
