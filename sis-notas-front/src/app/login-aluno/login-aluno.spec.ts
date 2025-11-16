import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginAluno } from './login-aluno';

describe('LoginAluno', () => {
  let component: LoginAluno;
  let fixture: ComponentFixture<LoginAluno>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginAluno]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginAluno);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
