import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment.prod';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  base: any = environment.apiUrl;
  constructor(private http: HttpClient) { }

  test(): any {
    const url = this.base + '/home';
    return this.http.get(url, {
      withCredentials: true  // <=========== important!
    });
  }
  connect_camera(): any {
    const url = this.base + '/connect_camera';
    return this.http.get(url, {
      withCredentials: true  // <=========== important!
    });
  }
  disconnect_camera(): any {
    const url = this.base + '/disconnect_camera';
    return this.http.get(url, {
      withCredentials: true  // <=========== important!
    });
  }
  get_urls(): any {
    const url = this.base + '/get_urls';
    return this.http.get(url, {
      withCredentials: true  // <=========== important!
    });
  }
  add_attendence(data): any {
    const url = this.base + '/add_attendance/';
    return this.http.post(url, {data:{data},
      withCredentials: true  // <=========== important!
    });
  }
  get_reports(): any {
    const url = this.base + '/get_reports';
    return this.http.get(url, {
      withCredentials: true  // <=========== important!
    });
  }
}
