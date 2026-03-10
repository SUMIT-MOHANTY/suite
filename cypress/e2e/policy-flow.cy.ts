describe('Policy issuance flow', () => {
  const captiveName = 'Test Captive E2E ' + Date.now();
  let captiveId = 0;

  beforeEach(() => {
    cy.visit('/');
    cy.login();
  });

  it('creates captive -> issues policy -> handles renewals', () => {
    // Navigate to captives page
    cy.contains('Captives').click();
    
    // Create new captive
    cy.get('[data-cy="create-captive"]').click();
    cy.get('input[name="name"]').type(captiveName);
    cy.get('input[name="domicile"]').type('Delaware');
    cy.get('input[name="inception_date"]').type('2024-01-01');
    cy.get('input[name="base_premium"]').type('1000000');
    cy.contains('button', 'Create').click();
    
    // Verify captive created and get ID
    cy.contains(captiveName).should('exist');
    cy.url().then(url => {
      const match = url.match(/captives\/(\d+)/);
      if (match) captiveId = parseInt(match[1]);
    });

    // Navigate to policies
    cy.contains('Policies').click();
    
    // Add new policy
    cy.contains('Issue Policy').click();
    
    // Step 1: Basic details
    cy.get('input[name="policy_number"]').type('POL-E2E-001');
    cy.get('input[placeholder="Select date"]').type('2024-01-15');
    cy.get('input[name="premium"]').type('50000');
    
    // Click next
    cy.contains('Next').click();
    
    // Step 2: Coverage details
    cy.get('input[name="coverage_limit"]').type('1000000');
    cy.get('input[name="deductible"]').type('10000');
    cy.get('textarea[name="notes"]').type('E2E test policy');
    
    // Submit
    cy.contains('Create Policy').click();
    
    // Verify policy in list
    cy.contains('POL-E2E-001').should('exist');
    cy.contains('$50,000').should('exist');
    
    // Test filtering
    cy.contains('Filter by status').parent().click();
    cy.contains('ACTIVE').click();
    cy.contains('POL-E2E-001').should('exist');
    
    // Test search
    cy.get('input[placeholder="Search policies"]').type('E2E');
    cy.contains('POL-E2E-001').should('exist');
    
    // Test export
    cy.get('button[aria-label="Download"]').first().click();
    cy.readFile('cypress/downloads/policy-1-binder.xlsx').should('exist');
    
    // Test upload ACORD
    cy.contains('Upload ACORD').click();
    cy.get('input[type="file"]').selectFile('cypress/fixtures/acord-template.xlsx', { force: true });
    cy.contains('Confirm').click();
    
    // Verify upload success
    cy.contains('uploaded successfully').should('exist');
  });

  it('handles policy renewals', () => {
    if (!captiveId) return;
    
    cy.visit(`/captives/${captiveId}/policies`);
    
    // Find first policy
    cy.get('table tbody tr').first().within(() => {
      cy.get('button').contains('Renew').click();
    });
    
    // Renewal modal
    cy.get('input[placeholder="Select date"]').type('2024-12-31');
    cy.contains('Renew Policy').click();
    
    // Verify new policy created
    cy.contains('POL-E2E-001-R').should('exist');
  });

  it('validates form inputs', () => {
    cy.visit(`/captives/${captiveId}/policies`);
    cy.contains('Issue Policy').click();
    
    // Try to submit empty form
    cy.contains('Create Policy').click();
    
    // Check validation messages
    cy.contains('Please enter policy number').should('exist');
    cy.contains('Please select effective date').should('exist');
    cy.contains('Please enter premium amount').should('exist');
  });
});
