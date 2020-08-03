import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-report-card',
  templateUrl: './report-card.component.html',
  styleUrls: ['./report-card.component.css']
})
export class ReportCardComponent implements OnInit {

  @Input() attendance_true:string;
  @Input() attendance_pred:string;
  @Input() food_true:string;
  @Input() food_pred:string;
  @Input() accuracy:string;
  @Input() date:string;
  @Input() discrepancy:string;

  constructor() { }

  ngOnInit(): void {
  }

}
