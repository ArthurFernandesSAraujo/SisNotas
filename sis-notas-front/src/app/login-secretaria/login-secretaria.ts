import { Component, OnInit } from '@angular/core';
import { Menu } from '../menu/menu';
import { Router } from '@angular/router';
import { MatTabsModule } from '@angular/material/tabs';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSelectModule } from '@angular/material/select';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatTooltipModule } from '@angular/material/tooltip';
import { CadastroAlunoModal } from '../cadastro-aluno-modal/cadastro-aluno-modal';
import { CadastroProfessorModal } from '../cadastro-professor-modal/cadastro-professor-modal';

interface Professor {
  id: number;
  nome: string;
  disciplina: string;
  telefone: string;
  status: string;
}

interface Aluno {
  id: number;
  nome: string;
  curso: string;
  idade: number;
  status: string;
}

@Component({
  selector: 'app-login-secretaria',
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
  templateUrl: './login-secretaria.html',
  styleUrl: './login-secretaria.css',
  standalone: true,
})
export class LoginSecretaria implements OnInit {

  public usuarioName!: string;

  // FILTROS
  filtroProfessor = '';
  filtroAluno = '';

  // COLUNAS
  displayedColumnsProfessores = ['id', 'nome', 'disciplina', 'telefone', 'status', 'actions'];
  displayedColumnsAlunos = ['id', 'nome', 'curso', 'idade', 'status', 'actions'];

  // DATASOURCES
  dataSourceProfessores: Professor[] = [];
  dataSourceAlunos: Aluno[] = [];

  constructor(
    private router: Router,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.usuarioName = sessionStorage.getItem('email') || '';

    this.carregarProfessores();
    this.carregarAlunos();
  }

  private carregarProfessores() {
    setTimeout(() => {
      this.dataSourceProfessores = [
        { id: 1, nome: "Ana Silva", disciplina: "Matemática", telefone: "(11) 98765-4321", status: "Ativo" },
        { id: 2, nome: "Carlos Costa", disciplina: "Português", telefone: "(11) 91234-5678", status: "Ativo" },
        { id: 3, nome: "Joana Pereira", disciplina: "História", telefone: "(11) 99887-7766", status: "Inativo" }
      ];
    }, 1000);
  }

  private carregarAlunos() {
    setTimeout(() => {
      this.dataSourceAlunos = [
        { id: 1, nome: "João Pedro", curso: "Matemática", idade: 16, status: "Ativo" },
        { id: 2, nome: "Mariana Lima", curso: "Português", idade: 17, status: "Ativo" },
        { id: 3, nome: "Felipe Souza", curso: "História", idade: 18, status: "Inativo" }
      ];
    }, 1200);
  }

  abrirCadastroProfessor() {
    const dialogRef = this.dialog.open(CadastroProfessorModal, {
      width: '500px',
      disableClose: true,
      data: {}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log('Professor cadastrado:', result);
        this.dataSourceProfessores.push({ id: this.dataSourceProfessores.length + 1, ...result });
      }
    });
  }

  abrirCadastroAluno() {
    const dialogRef = this.dialog.open(CadastroAlunoModal, {
      width: '500px',
      disableClose: true,
      data: {}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log('Aluno cadastrado:', result);
        this.dataSourceAlunos.push({ id: this.dataSourceAlunos.length + 1, ...result });
      }
    });
  }
}
