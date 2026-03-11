describe('Login -> Captive -> Policy -> Claim', () => {
  it('completes full user flow', () => {
    cy.visit('/login')
    cy.get('#email').type('admin@company.com')
    cy.get('#password').type('password')
    cy.get('button[type=submit]').click()
    
    cy.visit('/captives/new')
    cy.get('#name').type('Test Captive')
    cy.get('button[type=submit]').click()
    
    cy.visit('/policies/new')
    cy.contains('Create Policy').click()
    
    cy.visit('/claims/new')
    cy.contains('File Claim').click()
  })
})
