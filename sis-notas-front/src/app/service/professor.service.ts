import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProfessorService {

  private API = "http://localhost:8000/professores";

  constructor(private http: HttpClient) {}

  // ============================================
  // LISTAR PROFESSORES
  // ============================================
  listarProfessores(): Observable<any[]> {
    return this.http.get<any[]>(`${this.API}/`);
  }

  // ============================================
  // LISTAR MATÉRIAS DO PROFESSOR LOGADO
  // ============================================
  materiasDoProfessor(idProfessor: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.API}/${idProfessor}/materias`);
  }

  // ============================================
  // LISTAR ALUNOS DE UMA MATÉRIA
  // ============================================
  alunosDaMateria(idProfessor: number, idMateria: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.API}/${idProfessor}/materias/${idMateria}/alunos`);
  }

  // ============================================
  // SALVAR NOTA DO ALUNO
  // ============================================
  salvarNota(idAluno: number, idMateria: number, nota: number): Observable<any> {

    const params = new HttpParams()
      .set("idmateria", idMateria.toString())
      .set("nota", nota.toString());

    return this.http.post(`${this.API}/notas/${idAluno}`, {}, { params });
  }

}
