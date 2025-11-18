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

import { ProfessorService } from '../service/professor.service';

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

  displayedColumns = ['id', 'nome', 'nota'];

  materias: any[] = [];
  alunos: any[] = [];
  materiaSelecionada: number | null = null;

  idProfessorLogado: number = 0;

  constructor(private professorService: ProfessorService) {}

  // ========================================================
  // GARANTE QUE ESTAMOS NO NAVEGADOR (SSR/VITE SAFE)
  // ========================================================
  isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof sessionStorage !== 'undefined';
  }

  ngOnInit(): void {
    this.pegarProfessorLogado();
  }

  // ========================================================
  // PEGAR O ID DO PROFESSOR LOGADO NO SESSIONSTORAGE
  // ========================================================
  pegarProfessorLogado() {
    if (!this.isBrowser()) {
      console.warn("⚠ sessionStorage não está disponível (SSR/Vite)");
      return;
    }

    const usuario = sessionStorage.getItem("usuario");

    if (usuario) {
      const obj = JSON.parse(usuario);
      console.log("Objeto do usuário logado:", obj);
      this.idProfessorLogado = obj.id;  // agora pega o ID correto
    } else {
      this.idProfessorLogado = 0;
    }

    console.log("Professor logado:", this.idProfessorLogado);

    if (!!this.idProfessorLogado) {
      this.carregarMateriasDoProfessor(this.idProfessorLogado);
    }
  }

  // ========================================================
  // CARREGAR MATÉRIAS DO PROFESSOR LOGADO
  // ========================================================
  carregarMateriasDoProfessor(id: any) {
    this.professorService.materiasDoProfessor(id)
      .subscribe({
        next: (res) => {

          // MAPEIA PARA O FORMATO CORRETO DO DROPDOWN
          this.materias = res.map((m: any) => ({
            idmateria: m.idmateria,
            nome: m.nome
          }));

          console.log("Matérias carregadas:", this.materias);
        },
        error: () => alert("Erro ao carregar matérias do professor!")
      });
  }

  // ========================================================
  // CARREGAR ALUNOS AO TROCAR A MATÉRIA
  // ========================================================
  carregarAlunosDaMateria() {

    console.log('entrou')
    if (!this.materiaSelecionada) {
      this.alunos = [];
      return;
    }

    console.log(this.idProfessorLogado)
    console.log(this.materiaSelecionada)

    this.professorService.alunosDaMateria(
      this.idProfessorLogado,
      this.materiaSelecionada
    ).subscribe({
      next: (res) => {
        this.alunos = res;
        console.log("Alunos carregados:", res);
      },
      error: () => alert("Erro ao carregar alunos!")
    });
  }

  // ========================================================
  // SALVAR NOTA DO ALUNO
  // ========================================================
  salvarNota(aluno: any) {
    if (!this.materiaSelecionada) {
      alert("Escolha uma matéria primeiro!");
      return;
    }

    if (aluno.nota === null || aluno.nota === undefined || aluno.nota === "") {
      alert("Digite uma nota válida!");
      return;
    }

    this.professorService.salvarNota(
      aluno.idaluno,
      this.materiaSelecionada,
      aluno.nota
    ).subscribe({
      next: () => alert(`Nota salva com sucesso para ${aluno.nome}!`),
      error: () => alert("Erro ao salvar nota!")
    });
  }

}
