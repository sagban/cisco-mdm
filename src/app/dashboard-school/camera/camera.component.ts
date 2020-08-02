import { Component, OnInit } from '@angular/core';
import {DataService} from '../../_services/data.service';

@Component({
  selector: 'app-camera',
  templateUrl: './camera.component.html',
  styleUrls: ['./camera.component.css']
})
export class CameraComponent implements OnInit {

  private status: boolean= false;
  constructor(private dataService: DataService) { }

  ngOnInit(): void {
  }
  connect(){
    this.dataService.connect_camera().subscribe(res=>{
      this.status = res.status == 1;
    })
  }
  disconnect(){
    this.dataService.disconnect_camera().subscribe(res=>{
      this.status = res.status != 1;
    })
  }
  getStatus(){
    return this.status;
  }

}
