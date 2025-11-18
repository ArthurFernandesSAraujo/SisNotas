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
        mediaGeral: 5.4,
        disciplinas: [
          { nome: 'Geografia', nota: 5.4 }
        ]
      };

      this.valor = dadosAPI.mediaGeral;
      this.disciplinas = dadosAPI.disciplinas;

    }, 700); 
  }

}
