import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment.prod';


@Injectable({
  providedIn: 'root'
})
export class FormService {

  base: any = environment.apiUrl;
  constructor(private http: HttpClient) { }

  login(data: any): any {
    const url = this.base + '/login';
    return this.http.post(url, {data: data}, {
      withCredentials: true  // <=========== important!
    });
  }
}
