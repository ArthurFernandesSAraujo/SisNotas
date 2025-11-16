import { Routes } from '@angular/router';
import { LoginAluno } from './login-aluno/login-aluno';
import { LoginProfessor } from './login-professor/login-professor';
import { LoginSecretaria } from './login-secretaria/login-secretaria';
import { Login } from './login/login';

export const routes: Routes = [
    { path: '', component: Login },
    { path: 'pagina-aluno', component: LoginAluno },
    { path: 'pagina-professor', component: LoginProfessor },
    { path: 'pagina-secretaria', component: LoginSecretaria },
];
