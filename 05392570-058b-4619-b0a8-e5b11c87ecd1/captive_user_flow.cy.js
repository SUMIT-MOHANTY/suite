describe('Captive User Flow', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000');
  });
  it('should create a new captive', () => {
    cy.get('a[href*="create"]').click();
    cy.get('#id_name').type('Test Captive');
    cy.get('#id_jurisdiction').select('AVG');
    cy.get('#id_formation_date').type('2024-01-15');
    cy.get('#id_minimum_capital').type('500000');
    cy.get('#id_paid_up_capital').type('250000');
    cy.get('#id_surplus').type('50000');
    cy.get('form').submit();
    cy.contains('Test Captive').should('be.visible');
  });
});
