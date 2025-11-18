import { Component, OnInit } from '@angular/core';
import { Menu } from '../menu/menu';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// Angular Material
import { MatTabsModule } from '@angular/material/tabs';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSelectModule } from '@angular/material/select';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatTooltipModule } from '@angular/material/tooltip';

// Modais
import { CadastroAlunoModal } from '../cadastro-aluno-modal/cadastro-aluno-modal';
import { CadastroProfessorModal } from '../cadastro-professor-modal/cadastro-professor-modal';

// Serviços
import { SecretariaService } from '../service/secretaria.service';

interface Professor {
  id: number;
  nome: string;
  email: string;
}

interface Aluno {
  id: number;
  nome: string;
  matricula: string;
  email: string;
}

@Component({
  selector: 'app-login-secretaria',
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
  templateUrl: './login-secretaria.html',
  styleUrl: './login-secretaria.css'
})
export class LoginSecretaria implements OnInit {

  // FILTROS
  filtroProfessor = '';
  filtroAluno = '';

  // TABELAS
  displayedColumnsProfessores = ['id', 'nome', 'email', 'actions'];
  displayedColumnsAlunos = ['id', 'nome', 'matricula', 'email', 'actions'];
  displayedColumnsMaterias = ['id', 'nome', 'actions'];

  // DADOS
  dataSourceProfessores: Professor[] = [];
  dataSourceAlunos: Aluno[] = [];
  materias: any[] = [];

  // NOVA MATÉRIA
  novaMateria: string = '';

  // ASSOCIAÇÕES
  professorSelecionado: number | null = null;
  materiaSelecionadaProfessor: number | null = null;

  alunoSelecionado: number | null = null;
  materiaSelecionadaAluno: number | null = null;

  constructor(
    private router: Router,
    private dialog: MatDialog,
    private secretariaService: SecretariaService
  ) {}

  ngOnInit(): void {
    this.carregarProfessores();
    this.carregarAlunos();
    this.carregarMaterias();
  }

  // ===============================
  // PROFESSORES
  // ===============================

  carregarProfessores() {
    this.secretariaService.listarProfessores().subscribe({
      next: (res) => {
        this.dataSourceProfessores = res.map((p: any) => ({
          id: p.idprofessor,
          nome: p.nome,
          email: p.email
        }));
      },
      error: (err) => console.error("Erro ao carregar professores:", err)
    });
  }

  abrirCadastroProfessor() {
    const dialogRef = this.dialog.open(CadastroProfessorModal, {
      width: '500px',
      disableClose: true,
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.secretariaService.cadastrarProfessor(result).subscribe(() => {
          this.carregarProfessores();
        });
      }
    });
  }

  editarProfessor(prof: Professor) {
    const dialogRef = this.dialog.open(CadastroProfessorModal, {
      width: '500px',
      disableClose: true,
      data: prof
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.secretariaService.atualizarProfessor(prof.id, result).subscribe(() => {
          this.carregarProfessores();
        });
      }
    });
  }

  excluirProfessor(id: number) {
    this.secretariaService.excluirProfessor(id).subscribe(() => {
      this.carregarProfessores();
    });
  }

  // ===============================
  // ALUNOS
  // ===============================

  carregarAlunos() {
    this.secretariaService.listarAlunos().subscribe({
      next: (res) => {
        this.dataSourceAlunos = res.map((a: any) => ({
          id: a.idaluno,
          nome: a.nome,
          matricula: a.matricula,
          email: a.email
        }));
      },
      error: (err) => console.error("Erro ao carregar alunos:", err)
    });
  }

  abrirCadastroAluno() {
    const dialogRef = this.dialog.open(CadastroAlunoModal, {
      width: '500px',
      disableClose: true,
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.secretariaService.cadastrarAluno(result).subscribe(() => {
          this.carregarAlunos();
        });
      }
    });
  }

  editarAluno(aluno: Aluno) {
    const dialogRef = this.dialog.open(CadastroAlunoModal, {
      width: '500px',
      disableClose: true,
      data: aluno
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.secretariaService.atualizarAluno(aluno.id, result).subscribe(() => {
          this.carregarAlunos();
        });
      }
    });
  }

  excluirAluno(id: number) {
    this.secretariaService.excluirAluno(id).subscribe(() => {
      this.carregarAlunos();
    });
  }

  // ===============================
  // MATÉRIAS
  // ===============================

  carregarMaterias() {
    this.secretariaService.listarMaterias().subscribe({
      next: (res) => {
        this.materias = res;
      },
      error: () => alert("Erro ao carregar matérias!")
    });
  }

  cadastrarMateria() {
    if (!this.novaMateria.trim()) {
      alert("Digite o nome da matéria!");
      return;
    }

    this.secretariaService.cadastrarMateria({ nome: this.novaMateria }).subscribe({
      next: () => {
        this.novaMateria = '';
        this.carregarMaterias();
      },
      error: () => alert("Erro ao cadastrar matéria!")
    });
  }

  excluirMateria(id: number) {
    if (!confirm("Deseja realmente excluir esta matéria?")) return;

    this.secretariaService.excluirMateria(id).subscribe({
      next: () => this.carregarMaterias(),
      error: () => alert("Erro ao excluir matéria!")
    });
  }

  // ===============================
  // ASSOCIAÇÕES
  // ===============================

  associarProfessorMateria() {
    if (!this.professorSelecionado || !this.materiaSelecionadaProfessor) {
      alert("Selecione o professor e a matéria.");
      return;
    }

    this.secretariaService.associarProfessorMateria(
      this.professorSelecionado,
      this.materiaSelecionadaProfessor
    ).subscribe(() => alert("Professor associado!"));
  }

  associarAlunoMateria() {
    if (!this.alunoSelecionado || !this.materiaSelecionadaAluno) {
      alert("Selecione o aluno e a matéria.");
      return;
    }

    this.secretariaService.associarAlunoMateria(
      this.alunoSelecionado,
      this.materiaSelecionadaAluno
    ).subscribe(() => alert("Aluno associado!"));
  }

}
