import { Component, OnInit } from '@angular/core';
import {DataService} from '../../_services/data.service';
import {__await} from 'tslib';
import {max} from 'rxjs/internal/operators';

@Component({
  selector: 'app-camera',
  templateUrl: './camera.component.html',
  styleUrls: ['./camera.component.css']
})
export class CameraComponent implements OnInit {

  private status: boolean= false;
  public message: string = "Not Connected";
  public data:any = [];
  person_count:number = 0;
  show = -1
  constructor(private dataService: DataService) { }

  ngOnInit(): void {
  }
  async delay(ms: number) {
      return new Promise( resolve => setTimeout(resolve, ms) );
  }
  connect(){
    this.message = "Connecting Camera... ";
    this.delay(800);
    this.data = [];
    this.dataService.connect_camera().subscribe(res=>{
      this.status = res.status == 1;
      this.message = "Connected";

    })
  }
  disconnect(){
    this.message = "Stopping Camera... ";
    this.delay(800);
    this.message = "Fetching Head counts";
    this.delay(1500);
    this.dataService.disconnect_camera().subscribe(res=>{
      console.log(res);
      this.status = res.status != 1;
      this.delay(1500);
      if(res.status == 1 && res.data) {
        this.data = res.data;
        this.show = 0;
        if(this.data.length>0) this.person_count = this.data[this.data.length - 1]['person_count'];
        else{
          this.show = 0;
        }
      }
      else{

      }

      this.message = "Not Connected"

    });
  }
  getStatus(){
    return this.status;
  }

}
