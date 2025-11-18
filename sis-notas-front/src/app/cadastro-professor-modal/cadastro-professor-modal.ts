import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogRef, MatDialogActions, MatDialogContent } from '@angular/material/dialog';

@Component({
  selector: 'app-cadastro-professor-modal',
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
  templateUrl: './cadastro-professor-modal.html',
})
export class CadastroProfessorModal {

  formGroup: FormGroup;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<CadastroProfessorModal>
  ) {

    this.formGroup = this.fb.group({
      nome: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      usuario: ['', Validators.required],
      senha: ['', Validators.required],
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
