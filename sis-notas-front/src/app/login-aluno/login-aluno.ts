import { Component, OnInit } from '@angular/core';
import { Menu } from '../menu/menu';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login-aluno',
  imports: [
    Menu,
    CommonModule   
  ],
  templateUrl: './login-aluno.html',
  styleUrl: './login-aluno.css',
})
export class LoginAluno implements OnInit{

  public valor: any;
  public disciplinas: any[] = [];

  ngOnInit(): void {
    this.buscarNotaDoBackend();
    this.buscarDados();
  }

  buscarNotaDoBackend() {
    setTimeout(() => {
      this.valor = 7.5; 
    }, 500);
  }

   buscarDados() {
    setTimeout(() => {
      const dadosAPI = {
        mediaGeral: 7.2,
        disciplinas: [
          { nome: 'Matemática', nota: 8.5 },
          { nome: 'História', nota: 6.0 },
          { nome: 'Geografia', nota: 4.5 },
          { nome: 'Português', nota: 7.2 },
          { nome: 'Física', nota: 5.4 }
        ]
      };

      this.valor = dadosAPI.mediaGeral;
      this.disciplinas = dadosAPI.disciplinas;

    }, 700); 
  }

}
