import { Component, OnInit } from '@angular/core';
import {DataService} from '../../_services/data.service';
import {AuthenticationService} from '../../_services/authentication.service';
import {ActivatedRoute, Router} from '@angular/router';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {FormService} from '../../_services/form.service';

@Component({
  selector: 'app-add',
  templateUrl: './add.component.html',
  styleUrls: ['./add.component.css']
})
export class AddComponent implements OnInit {
  public message: string;
  addForm: FormGroup;

  constructor(private route: ActivatedRoute,
              private router: Router,
              private fb: FormBuilder,
              // private formService: FormService,
              private datService: DataService,
              private authenticationService: AuthenticationService
  ) { }
  ngOnInit(): void {
    this.addForm = this.fb.group({
      attendance: ['', [Validators.required]],
      food: ['', [Validators.required]],
    });

  }
  get f() { return this.addForm.controls; }

  onsubmit(){
    this.datService.add_attendence(this.addForm.value).subscribe(res=>{
      if(res.status == 1)this.message = "Attendance saved";
      console.log(res)
    })
  }

}
