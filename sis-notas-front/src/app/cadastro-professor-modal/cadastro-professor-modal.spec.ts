import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CadastroProfessorModal } from './cadastro-professor-modal';

describe('CadastroProfessorModal', () => {
  let component: CadastroProfessorModal;
  let fixture: ComponentFixture<CadastroProfessorModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CadastroProfessorModal]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CadastroProfessorModal);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
