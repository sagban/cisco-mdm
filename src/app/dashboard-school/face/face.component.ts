import { Component, OnInit } from '@angular/core';
import {DataService} from '../../_services/data.service';

@Component({
  selector: 'app-face',
  templateUrl: './face.component.html',
  styleUrls: ['./face.component.css']
})
export class FaceComponent implements OnInit {

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.dataService.do_face_recognition().subscribe(res=>{
      console.log(res);
    })
  }

}
