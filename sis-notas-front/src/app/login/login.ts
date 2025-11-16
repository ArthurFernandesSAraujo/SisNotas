import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { Router, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [
    RouterOutlet,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    ReactiveFormsModule,
    CommonModule,
  ],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login implements OnInit {

  formGroup!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.initForm();
  }

  initForm() {
    this.formGroup = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      senha: ['', Validators.required],
      perfil: ['', Validators.required]
    });
  }

  redirectFunction() {
    console.log('E-mail:', this.formGroup.value.email);
    console.log('Senha:', this.formGroup.value.senha);
    console.log('Perfil:', this.formGroup.value.perfil);

    const perfil = this.formGroup.value.perfil;
    const email =  this.formGroup.value.email
    const senha = this.formGroup.value.senha

    sessionStorage.setItem('email', email);
    sessionStorage.setItem('senha', senha);     
    sessionStorage.setItem('perfil', perfil);

    if (perfil === 'secretaria') sessionStorage.setItem('menuColor', '#8e44ad');
    if (perfil === 'professor') sessionStorage.setItem('menuColor', '#2980b9');
    if (perfil === 'aluno') sessionStorage.setItem('menuColor', '#27ae60');


    if (perfil == 'secretaria') {
      this.router.navigate(['/pagina-secretaria']);
    }

    if (perfil === 'professor') {
      this.router.navigate(['/pagina-professor']);
    }

    if (perfil === 'aluno') {
      this.router.navigate(['/pagina-aluno']);
    }
    
  }

  get email() { return this.formGroup.get('email'); }
  get senha() { return this.formGroup.get('senha'); }
  get perfil() { return this.formGroup.get('perfil'); }
}
