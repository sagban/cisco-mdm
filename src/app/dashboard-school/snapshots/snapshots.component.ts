import { Component, OnInit } from '@angular/core';
import {DataService} from '../../_services/data.service';

@Component({
  selector: 'app-snapshots',
  templateUrl: './snapshots.component.html',
  styleUrls: ['./snapshots.component.css']
})
export class SnapshotsComponent implements OnInit {

  urls=[];
  public message: string;
  constructor(private dataservice:DataService) { }

  ngOnInit(): void {
    this.geturls()
  }
  geturls(){
    this.message = "We are fetching the results for you. It might take 1 - 2 minutes";
    this.dataservice.get_urls().subscribe(res=>{
      if(res.status ==1){
        console.log(res.data);
        this.urls = res.data;
        this.message = "Snapshots received"
      }
      if(this.urls.length == 0)this.message = "We coudn't fount any snapshots"
    });
  }

}
