import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginSecretaria } from './login-secretaria';

describe('LoginSecretaria', () => {
  let component: LoginSecretaria;
  let fixture: ComponentFixture<LoginSecretaria>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginSecretaria]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginSecretaria);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
