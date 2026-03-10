# Final SWOT Analysis & Handoff Summary

## Strengths
- ✅ Working full-stack architecture authenticated SPA
- ✅ Clean separation: React frontend + Express backend
- ✅ Type-safe APIs with TypeScript end-to-end
- ✅ Docker containerisation ready for staging/prod
- ✅ Health check & CRUD endpoints tested

## Weaknesses
- No structured logging or APM in production
- SQLite only in dev, PostgreSQL needs full migration scripts
- Authentication uses JWTs with no refresh token rotation
- No rate limiting or brute-force protections
- Missing integration tests at edge boundaries
- No environment readiness checks (network, DB, secrets)

## Opportunities
- Add Prometheus metrics & Grafana dashboards
- Convert to micro-front-ends for outsourced development
- Plug in Auth0 or AWS Cognito for SSO
- Deploy to AWS ECS Fargate with Blue-Green pipelines
- Break backend into GraphQL gateway + service mesh

## Threats
- Single-node SQLite will corrupt under concurrent writes
- Secrets are loaded from environment variables = runtime leaks
- No WAF/DDoS protections on edge gateway
- Hard-coded CORS will break multi-domain auth in staging
- Vite dev server proxy is not production-secure (localhost bypass)

## Open Risks (Scope & Compliance)
1. **GDPR/PII**: todo titles may include user-assigned personal data; no audit trail
2. **Licensing**: Used MIT templates--verify transitive dependencies AGPL/GPL
3. **OWASP Top 10**: No CSRF tokens, session cookies are http-only false by default
4. **Bitmask Port Collisions**: HOST_PORT env flag can clash with host firewall rules
5. **Data Loss**: No WAL on SQLite; dev deployments can accidentally nuke `/backend/data`

## Stakeholder Questions for Next Discovery
- Should todos support multi-user sharing and RBAC?
- Target uptime SLA? (affects PostgreSQL HA choice)
- Regulatory jurisdictions: EU (GDPR), US (CCPA)?
- Budget for managed DB vs self-hosted?
- Preferred CDN edge cache invalidation strategy?
- Secrets: Vault, AWS SSM, or sealed secrets?
