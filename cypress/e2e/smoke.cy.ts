describe("Smoke", () => {
  it("loads", () => {
    cy.visit("/");
    cy.contains("Todo List");
  });
});
