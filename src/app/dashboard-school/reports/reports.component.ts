import { Component, OnInit } from '@angular/core';
import {DataService} from '../../_services/data.service';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.css']
})
export class ReportsComponent implements OnInit {

  reports = [];
  message = "No reports found";
  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.dataService.get_reports().subscribe(res=>{
      if(res.status == 1){
        console.log(res.data);
        this.reports = res.data;
        this.message = "Reports Found"
      }
    })
  }



}
