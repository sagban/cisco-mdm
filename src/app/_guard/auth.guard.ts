import { Injectable } from '@angular/core';
import {Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree} from '@angular/router';
import { AuthenticationService } from '../_services/authentication.service';
import {Observable} from "rxjs/index";


@Injectable({ providedIn: 'root' })

export class AuthGuard implements CanActivate {
  constructor(
      private router: Router,
      private authenticationService: AuthenticationService
  ) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {

    const value = this.authenticationService.getSession();

    if (value === true) {
      return true;
    }
    else{
      this.router.navigate(['../login'], { queryParams: { returnUrl: state.url } });
      return false;
    }
  }

}
