import {Component, Input, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {FormService} from "../_services/form.service";
import {ActivatedRoute, Router} from "@angular/router";
import {AuthenticationService} from "../_services/authentication.service";
import {first} from "rxjs/internal/operators";
import {environment} from '../../environments/environment';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  message: string = "";
  loginForm:FormGroup;
  returnUrl: string;
  constructor(private route: ActivatedRoute,
              private router: Router,
              private fb: FormBuilder,
              private formService: FormService,
              private authenticationService: AuthenticationService
  ) { }

  ngOnInit() {

    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/dashboard';
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      role: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(8)]]
    });
  }

  // convenience getter for easy access to form fields
  get f() { return this.loginForm.controls; }

  signIn() {
    this.formService.login(this.loginForm.value).pipe(first()).subscribe(res =>{
      console.log(res);
      if(res.status == 0){
        this.message = res.message;
      }
      else if(res.status == 1 || res.status == 2){
        this.message = res.message;
        this.loginForm.reset();
        localStorage.setItem('session', JSON.stringify(true));
        this.authenticationService._getSession.next(true);
        localStorage.setItem('verifiedUserName', JSON.stringify(res.data['username']));
        // this.authenticationService._getVerifiedUserName.next( res.data['username']);
        // window.location.href = this.returnUrl;
      }
      else{
        this.message = "Something went wrong";
      }
    });
  }

}
