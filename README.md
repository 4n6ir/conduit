# conduit

Aqueduct bundles AWS Cloud Development Kit (CDK) projects to deploy or destroy in parallel to accounts in the bootstrapped organization.

The app.py configuration from the project handles specific regions or will default to the deployed region.

Conduit picks up the bundle from an S3 bucket for deployment or destruction using a lambda fan-out pattern.

##### TO-DO:

- [ ] Build Docker Containers
- [ ] Long Running Deployments
