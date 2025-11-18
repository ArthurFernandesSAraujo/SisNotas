import { Routes } from '@angular/router';

import { Login } from './login/login';
import { LoginAluno } from './login-aluno/login-aluno';
import { LoginProfessor } from './login-professor/login-professor';
import { LoginSecretaria } from './login-secretaria/login-secretaria';

export const routes: Routes = [
  { path: '', component: Login },
  { path: 'pagina-aluno', component: LoginAluno },
  { path: 'pagina-professor', component: LoginProfessor },
  { path: 'pagina-secretaria', component: LoginSecretaria },
  { path: '**', redirectTo: '' }
];
