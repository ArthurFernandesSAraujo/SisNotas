import { Component, OnInit } from '@angular/core';
import { Menu } from '../menu/menu';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { MatTooltipModule } from '@angular/material/tooltip';

@Component({
  selector: 'app-login-professor',
  standalone: true,
  imports: [
    Menu,
    CommonModule,
    FormsModule,
    MatTabsModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatButtonModule,
    MatSelectModule,
    MatTableModule,
    MatPaginatorModule,
    MatDialogModule,
    MatTooltipModule
  ],
  templateUrl: './login-professor.html',
  styleUrl: './login-professor.css',
})
export class LoginProfessor implements OnInit {

  displayedColumns = ['id', 'nome', 'disciplina', 'status', 'nota'];

  // Simulando dados de um endpoint
  dataSource = [
    { id: 1, nome: 'João', disciplina: 'Matemática', status: 'Ativo', nota: null },
    { id: 2, nome: 'Maria', disciplina: 'Português', status: 'Ativo', nota: 7 },
    { id: 3, nome: 'Carlos', disciplina: 'História', status: 'Ativo', nota: null }
  ];

  ngOnInit(): void {}

  salvarNota(aluno: any) {
    if (aluno.nota !== null && aluno.nota !== undefined) {
      console.log(`Salvando nota do aluno ${aluno.nome}: ${aluno.nota}`);
      alert(`Nota do ${aluno.nome} salva: ${aluno.nota}`);
      // Aqui você chamaria o endpoint real via HttpClient
    } else {
      alert(`Digite uma nota válida para ${aluno.nome}`);
    }
  }
}
