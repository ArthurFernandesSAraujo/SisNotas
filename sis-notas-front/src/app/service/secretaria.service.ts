import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SecretariaService {

  private baseUrlSecretaria = 'http://localhost:8000/secretaria';
  private baseUrlMaterias = 'http://localhost:8000/materias';
  private baseUrlAssociacoes = 'http://localhost:8000/associacoes';

  constructor(private http: HttpClient) {}

  // ============================================
  // PROFESSORES
  // ============================================
  listarProfessores(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrlSecretaria}/professores`);
  }

  cadastrarProfessor(data: any): Observable<any> {
    return this.http.post(`${this.baseUrlSecretaria}/professores`, data);
  }

  atualizarProfessor(id: number, data: any): Observable<any> {
    return this.http.put(`${this.baseUrlSecretaria}/professores/${id}`, data);
  }

  excluirProfessor(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrlSecretaria}/professores/${id}`);
  }

  // ============================================
  // ALUNOS
  // ============================================
  listarAlunos(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrlSecretaria}/alunos`);
  }

  cadastrarAluno(data: any): Observable<any> {
    return this.http.post(`${this.baseUrlSecretaria}/alunos`, data);
  }

  atualizarAluno(id: number, data: any): Observable<any> {
    return this.http.put(`${this.baseUrlSecretaria}/alunos/${id}`, data);
  }

  excluirAluno(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrlSecretaria}/alunos/${id}`);
  }

  // ============================================
  // MATÉRIAS
  // ============================================
  listarMaterias(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrlMaterias}/`);
  }

  cadastrarMateria(data: any): Observable<any> {
    const params = new HttpParams().set('nome', data.nome);
    return this.http.post(`${this.baseUrlMaterias}/`, null, { params });
  }

  excluirMateria(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrlMaterias}/${id}`);
  }

  // ============================================
  // ASSOCIAÇÕES (ALUNO x MATÉRIA / PROFESSOR x MATÉRIA)
  // ============================================

  associarAlunoMateria(idaluno: number, idmateria: number): Observable<any> {
    const params = new HttpParams()
      .set('idaluno', idaluno)
      .set('idmateria', idmateria);

    return this.http.post(`${this.baseUrlAssociacoes}/aluno-materia`, null, { params });
  }

  associarProfessorMateria(idprofessor: number, idmateria: number): Observable<any> {
    const params = new HttpParams()
      .set('idprofessor', idprofessor)
      .set('idmateria', idmateria);

    return this.http.post(`${this.baseUrlAssociacoes}/professor-materia`, null, { params });
  }

}
