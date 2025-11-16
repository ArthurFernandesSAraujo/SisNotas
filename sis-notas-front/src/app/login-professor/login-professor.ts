import { Component, OnInit } from '@angular/core';
import { Menu } from '../menu/menu';

@Component({
  selector: 'app-login-professor',
  imports: [Menu],
  templateUrl: './login-professor.html',
  styleUrl: './login-professor.css',
})
export class LoginProfessor implements OnInit{

  ngOnInit(): void {
  }

}
