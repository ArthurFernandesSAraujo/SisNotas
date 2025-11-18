import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule  
  ],
  templateUrl: './menu.html',
  styleUrl: './menu.css',
})
export class Menu implements OnInit {

  obj: any;
  menuColor = '';
  userEmail = '';
  userRole = '';

  constructor(private router: Router) {}

  // Verifica se está no navegador para evitar erros em SSR/Vite
  isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof sessionStorage !== 'undefined';
  }

  ngOnInit(): void {

    const usuario = sessionStorage.getItem("usuario");

    if (usuario) {
       this.obj = JSON.parse(usuario);
      console.log("Objeto do usuário logado:", this.obj.nome);
    }

    if (this.isBrowser()) {
      this.menuColor = sessionStorage.getItem('menuColor') || '#000';
     this.userEmail = sessionStorage.getItem(this.obj.nome) || '';
       this.userRole = sessionStorage.getItem('perfil') || '';
    }
  }

  logout() {
    if (this.isBrowser()) {
      sessionStorage.clear();
    }
    this.router.navigate(['/']);
  }
}
