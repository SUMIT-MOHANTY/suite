declare global {
  namespace Cypress {
    interface Chainable {
      login(): Chainable<void>
    }
  }
}

Cypress.Commands.add('login', () => {
  cy.fixture('user').then(({ email, password }) => {
    cy.session([email, password], () => {
      cy.request('POST', '/api/auth/login', { email, password })
    })
  })
})
