import { Injectable } from '@angular/core';
import {
  Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree,
  ActivatedRoute, ParamMap
} from '@angular/router';

import {Observable} from "rxjs/index";
import {map} from "rxjs/operators";



@Injectable({ providedIn: 'root' })

export class UserGuard implements CanActivate {
  constructor(
      private router: Router

  ) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    const val = UserGuard.validUserName(route.paramMap.get('username'));
    if(!val)this.router.navigate(['../404']);
    return val;
  }

  private static validUserName(str):boolean{
    const p = new RegExp("^@[a-z0-9_-]{3,15}$");
    return p.test(str);
  }

}
