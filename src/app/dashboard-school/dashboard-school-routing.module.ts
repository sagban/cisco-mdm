import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {AuthGuard} from "../_guard/auth.guard";
import {DashboardSchoolComponent} from './dashboard-school.component';
import {HomeComponent} from './home/home.component';
import {CameraComponent} from './camera/camera.component';
import {ReportsComponent} from './reports/reports.component';
import {GrievanceComponent} from './grievance/grievance.component';
import {SnapshotsComponent} from './snapshots/snapshots.component';
import {AddComponent} from './add/add.component';
import {FaceComponent} from './face/face.component';

const routes: Routes = [
  {
    path : "dashboard/school",
    component: DashboardSchoolComponent,
    canActivate: [AuthGuard],
    children: [
      // { path: "", component: HomeComponent, canActivate: [AuthGuard]},
      { path: "", component: CameraComponent, canActivate: [AuthGuard]},
      { path: "snapshots", component: SnapshotsComponent, canActivate: [AuthGuard]},
      { path: "reports", component: ReportsComponent, canActivate: [AuthGuard]},
      { path: "grievance", component: GrievanceComponent, canActivate: [AuthGuard]},
      { path: "add", component: AddComponent, canActivate: [AuthGuard]},
      { path: "face", component: FaceComponent, canActivate: [AuthGuard]},
    ]
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DashboardSchoolRoutingModule { }
