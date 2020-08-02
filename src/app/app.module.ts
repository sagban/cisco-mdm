import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { DashboardSchoolModule} from './dashboard-school/dashboard-school.module';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { AboutComponent } from './about/about.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { ReportsComponent } from './reports/reports.component';
import { LoginHomeComponent } from './login-home/login-home.component';
import { HttpClientModule} from '@angular/common/http';
import { FormsModule, ReactiveFormsModule} from '@angular/forms';
import { AuthenticationService} from './_services/authentication.service';
import { BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { DashboardSchoolComponent } from './dashboard-school/dashboard-school.component';
import { DashboardAdminComponent } from './dashboard-admin/dashboard-admin.component';
import { ReportCardComponent } from './report-card/report-card.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    HeaderComponent,
    FooterComponent,
    AboutComponent,
    LoginComponent,
    SignupComponent,
    ForgotPasswordComponent,
    ReportsComponent,
    LoginHomeComponent,
    DashboardSchoolComponent,
    DashboardAdminComponent,
    ReportCardComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    DashboardSchoolModule,
    AppRoutingModule
  ],
  providers: [AuthenticationService],
  bootstrap: [AppComponent]
})
export class AppModule { }
