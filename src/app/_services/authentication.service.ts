import {Injectable} from '@angular/core';
import { environment } from '../../environments/environment';
import {HttpClient} from "@angular/common/http";
import {BehaviorSubject, Observable} from "rxjs/index";
@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  public _getSession: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(JSON.parse(localStorage.getItem('session')));
  public getSessionEmitter: Observable<boolean> = this._getSession.asObservable();

  public _getVerified: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(JSON.parse(localStorage.getItem('verified')));
  public getVerifiedEmitter: Observable<boolean> = this._getVerified.asObservable();
  public _getVerifiedEmail: BehaviorSubject<string> = new BehaviorSubject<string>(localStorage.getItem('verifiedEmail'));
  public getVerifiedEmailEmitter: Observable<string> = this._getVerifiedEmail.asObservable();
  public _getVerifiedUserName: BehaviorSubject<string> = new BehaviorSubject<string>(localStorage.getItem('verifiedUserName'));
  public getVerifiedUserNameEmitter: Observable<string> = this._getVerifiedUserName.asObservable();
  session:boolean;
  base: any = environment.apiUrl;
  constructor(private http: HttpClient) {
  }

  checkSession(): any {
    const url = this.base + '/check';
    return this.http.get(url, {
      withCredentials: true  // <=========== important!
    });
  }

  getSession(){
    return this._getSession.value;
  }
  getVerified(){
    return this._getVerified.value;
  }
  getUserName(){
    return this._getVerifiedUserName.value;
  }

  logout(): any {
    const url = this.base + '/logout';
    return this.http.get(url, {
      withCredentials: true  // <=========== important!
    });
  }
}
