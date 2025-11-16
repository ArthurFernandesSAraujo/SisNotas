import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-menu',
  imports: [CommonModule],
  templateUrl: './menu.html',
  styleUrl: './menu.css',
})
export class Menu implements OnInit {


  menuColor = '';
  userEmail = '';
  userRole = '';

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.menuColor = sessionStorage.getItem('menuColor') || '#000';
    this.userEmail = sessionStorage.getItem('email') || '';
    this.userRole = sessionStorage.getItem('perfil') || '';
  }

  logout() {
    sessionStorage.clear();
    this.router.navigate(['/']);
  }
}