import { Component, OnInit } from '@angular/core';
import { Menu } from '../menu/menu';

@Component({
  selector: 'app-login-aluno',
  imports: [Menu],
  templateUrl: './login-aluno.html',
  styleUrl: './login-aluno.css',
})
export class LoginAluno implements OnInit{

  ngOnInit(): void {
  }

}
