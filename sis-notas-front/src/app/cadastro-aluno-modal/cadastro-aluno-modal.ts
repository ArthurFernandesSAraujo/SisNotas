import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogActions, MatDialogContent, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { CadastroProfessorModal } from '../cadastro-professor-modal/cadastro-professor-modal';

@Component({
  selector: 'app-cadastro-aluno-modal',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatDialogActions,
    MatDialogContent
],
  templateUrl: './cadastro-aluno-modal.html',
  styleUrl: './cadastro-aluno-modal.css',
})
export class CadastroAlunoModal {
   formGroup: FormGroup;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<CadastroProfessorModal>
  ) {
    this.formGroup = this.fb.group({
      nome: ['', Validators.required],
      disciplina: ['', Validators.required],
      telefone: ['', Validators.required],
      senha: ['', Validators.required],
      email: ['', Validators.required, Validators.email],
      status: ['Ativo', Validators.required],
      senhaConfirmar: ['', Validators.required]
    });
  }

  salvar() {
    if (this.formGroup.valid) {
      this.dialogRef.close(this.formGroup.value);
    }
  }

  cancelar() {
    this.dialogRef.close();
  }

}
