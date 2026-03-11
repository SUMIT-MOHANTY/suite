describe('end-to-end captive -> policy -> claim flow', () => {
  beforeEach(() => {
    cy.login()
  })

  it('creates a captive, adds a policy, files a claim', () => {
    // 1. Create captive
    cy.visit('/captives')
    cy.findByRole('button', { name: /new captive/i }).click()
    cy.findByLabelText(/name/i).type('Cypress Captive Inc')
    cy.findByLabelText(/domicile/i).type('Delaware')
    cy.findByLabelText(/base premium/i).clear().type('500000')
    cy.get('input[name="inception_date"]').invoke('val', '2024-01-01').trigger('change')
    cy.findByRole('button', { name: /save/i }).click()
    cy.url().should('match', /\/captives\/\d+$/)

    cy.get('h1').invoke('text').then(str => {
      const captiveId = Number(str.split('/').pop())

      // 2. Issue Policy
      cy.visit(`/policies`)
      cy.findByRole('button', { name: /new policy/i }).click()
      cy.findByLabelText(/captive/i).select(String(captiveId))
      cy.findByLabelText(/policy number/i).type('POL-E2E-001')
      cy.get('input[name="effective_date"]').invoke('val', '2024-02-01').trigger('change')
      cy.findByLabelText(/premium/i).clear().type('250000')
      cy.findByRole('button', { name: /create/i }).click()
      cy.url().should('match', /\/policies\/\d+$/)

      cy.get('h1').invoke('text').then(str2 => {
        const policyId = Number(str2.split('/').pop())

        // 3. File Claim
        cy.visit(`/claims`)
        cy.findByRole('button', { name: /new claim/i }).click()
        cy.findByLabelText(/policy/i).select(String(policyId))
        cy.get('input[name="incident_date"]').invoke('val', '2024-07-05').trigger('change')
        cy.findByLabelText(/description/i).type('E2E test claim')
        cy.findByLabelText(/amount claimed/i).clear().type('80000')
        cy.findByRole('button', { name: /file claim/i }).click()
        cy.url().should('match', /\/claims\/\d+$/)
      })
    })
  })
})
