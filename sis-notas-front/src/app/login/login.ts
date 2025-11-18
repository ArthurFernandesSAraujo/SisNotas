import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { AuthService } from '../service/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    ReactiveFormsModule,
    CommonModule
  ],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login implements OnInit {

  formGroup!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.initForm();
  }

  initForm() {
    this.formGroup = this.fb.group({
      email: ['', Validators.required],   // <-- CORRIGIDO AQUI
      senha: ['', Validators.required],
      perfil: ['', Validators.required]
    });
  }

  redirectFunction() {

    if (this.formGroup.invalid) return;

    const credentials = {
      username: this.formGroup.value.email,
      senha: this.formGroup.value.senha,
      tipo: this.formGroup.value.perfil
    };

    this.authService.login(credentials).subscribe({
      next: (user) => {
        console.log("LOGIN OK:", user);

        sessionStorage.setItem("email", this.formGroup.value.email);
        sessionStorage.setItem("id_usuario", user.id.toString());
        sessionStorage.setItem("token", user.token);
        sessionStorage.setItem("usuario", JSON.stringify(user.nome));
        sessionStorage.setItem("perfil", user.nivel);

        if (user.nivel === 'secretaria') sessionStorage.setItem('menuColor', '#8e44ad');
        if (user.nivel === 'professor') sessionStorage.setItem('menuColor', '#2980b9');
        if (user.nivel === 'aluno') sessionStorage.setItem('menuColor', '#27ae60');

        if (user.nivel === 'secretaria') this.router.navigate(['/pagina-secretaria']);
        if (user.nivel === 'professor') this.router.navigate(['/pagina-professor']);
        if (user.nivel === 'aluno') this.router.navigate(['/pagina-aluno']);
      },

      error: (err) => {
        console.error("ERRO NO LOGIN:", err);
        alert(err.error.detail || "Erro ao fazer login");
      }
    });
  }

  get email() { return this.formGroup.get('email'); }
  get senha() { return this.formGroup.get('senha'); }
  get perfil() { return this.formGroup.get('perfil'); }
}
