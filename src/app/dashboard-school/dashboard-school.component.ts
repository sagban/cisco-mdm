import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {FormBuilder} from '@angular/forms';
import {AuthenticationService} from '../_services/authentication.service';
import {map} from "rxjs/operators";
@Component({
  selector: 'app-dashboard-school',
  templateUrl: './dashboard-school.component.html',
  styleUrls: ['./dashboard-school.component.css']
})
export class DashboardSchoolComponent implements OnInit {

  public menuListShown:Boolean = true;
  session:boolean= false;
  username:string = null;
  constructor(private route: ActivatedRoute,
              private router: Router,
              private fb: FormBuilder,
              public authenticationService: AuthenticationService
  ) {
    this.checkSession();
  }
  ngOnInit() {

    if(window.innerWidth <=600){
      this.menuListShown = false;
    }
    this.authenticationService.getVerifiedUserNameEmitter.subscribe(res=>{
      this.username = JSON.parse(res);
    });
    this.authenticationService.getSessionEmitter.subscribe(res=>{
      this.session = res;
    });

  }
  public toogleMenuList():void {
    if(window.innerWidth <=600){
      this.menuListShown = !this.menuListShown;
    }
  }
  public logout():void {
    this.authenticationService.logout().subscribe(res=>{
      if(res.status == 1){
        this.setKeys(false, null);
        this.router.navigate(['/sell_your_design']);
      }
    });
  }
  private checkSession(){
    this.authenticationService.checkSession().pipe(map(value =>{
      if (value['status'] === 1){
        this.setKeys(true, value['data']['username']);
      }
      else this.setKeys(false, null);

    }));
  }

  private setKeys(session:boolean, username:string){
    localStorage.setItem('session', JSON.stringify(session));
    this.authenticationService._getSession.next(session);
    localStorage.setItem('verifiedUserName', JSON.stringify(username));
    this.authenticationService._getVerifiedUserName.next( username);
  }

}
