import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginProfessor } from './login-professor';

describe('LoginProfessor', () => {
  let component: LoginProfessor;
  let fixture: ComponentFixture<LoginProfessor>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginProfessor]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginProfessor);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
