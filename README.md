# conduit

Aqueduct bundles AWS Cloud Development Kit (CDK) projects with updated account and region information to deploy or destroy in parallel to a bootstrapped organization.

Conduit picks up the bundle from an S3 bucket for deployment or destruction using a lambda fan-out pattern.