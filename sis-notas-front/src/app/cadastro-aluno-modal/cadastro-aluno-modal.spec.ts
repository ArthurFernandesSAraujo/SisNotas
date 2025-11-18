import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CadastroAlunoModal } from './cadastro-aluno-modal';

describe('CadastroAlunoModal', () => {
  let component: CadastroAlunoModal;
  let fixture: ComponentFixture<CadastroAlunoModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CadastroAlunoModal]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CadastroAlunoModal);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
