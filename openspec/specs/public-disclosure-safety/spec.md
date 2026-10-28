# Public Disclosure Safety

## Purpose
Canonical portfolio-only publication boundaries; no private product implementation.

## Requirements

### Requirement: Public-only source
The profile SHALL publish only explicitly curated public portfolio material and SHALL exclude secrets, private infrastructure identifiers, customer data, private source code and raw operational exports.

#### Scenario: A private credential-bearing file is proposed
- **WHEN** a change introduces a private key, credential assignment or forbidden sensitive file type
- **THEN** the public portfolio validation SHALL reject the change before publication

#### Scenario: Public case-study metadata is added
- **WHEN** a project entry is added to the public portfolio manifest
- **THEN** the validator SHALL require a unique project identifier and an existing referenced case study surfaced from the public README

### Requirement: Independently validated specifications
The repository SHALL retain official OpenSpec configuration and SHALL validate its tracked specification artifacts with the official OpenSpec CLI in a source-only GitHub Actions job.

#### Scenario: Proposed specification change
- **WHEN** a pull request updates OpenSpec artifacts
- **THEN** the source-only validation SHALL run the official parser and SHALL fail when strict validation reports invalid artifacts

### Requirement: Safe temporary branch lifecycle
A temporary branch SHALL be deleted only after its exact head is integrated into main, a matching repository-owned deletion intent exists, and the live ref has not moved.

#### Scenario: An unmerged or moved branch is examined
- **WHEN** a branch has no exact merged PR head or its live reference differs from the reviewed head
- **THEN** the cleanup workflow SHALL preserve it
