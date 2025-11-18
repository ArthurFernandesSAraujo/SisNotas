import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private baseUrl = 'http://localhost:8000/auth';

  constructor(private http: HttpClient) {}

  login(credentials: { username: string; senha: string; tipo: string }): Observable<any> {
    return this.http.post(`${this.baseUrl}/login`, credentials);
  }
}
