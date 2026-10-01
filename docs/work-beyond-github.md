# Work that does not live under this GitHub account

A lot of my professional work is in company repositories, client repositories or systems that predate this account. I do not copy that code here. What I can share is the context, the part I worked on and the decisions that mattered.

## SoftMarketing / Positivo — 2013–2014

I worked on PHP/Zend Framework and JavaScript modules for clients including Volvo, Baterias Moura and Positivo.

For Positivo, the work included a real-time call-center sales/calls dashboard and a Node.js + Asterisk integration.

**Used:** PHP · Zend Framework 2 · JavaScript · Node.js 0.x · Asterisk

## Nabile / Subway — 2015–2018

A franchise-management platform for Subway. I spent the first months building most of the system before the work was expanded to a larger team.

One unusual part was a visual editor for franchisees, tied to graphic production and print delivery.

**Used:** Laravel · Blade · jQuery · MySQL

## GoTrend — 2020–2022

Backend and database work for an e-commerce/SaaS platform with multi-level and financial rules. I was one of two developers for a significant part of the work and took ownership of backend/database concerns.

This included internal-balance flows, database design, procedures/indexing/partitioning and invoicing integration.

**Used:** PHP · MariaDB · JavaScript · Java · DigitalOcean

## Feat's / Unick — platform modernization

This is one of the projects that best explains how I approach legacy systems.

The platform had more than **4 million registered users**. The work was not a full rewrite. I helped lead a team of six through an incremental modernization: PHP legacy remained part of the picture while a Node.js/TypeScript API and Vue/TypeScript frontend were introduced.

The first major modernization phase took roughly **three months**. Processing paths that could take minutes were brought down to seconds or below in the cases documented at the time.

**Used:** PHP · Node.js · TypeScript · Vue.js · MariaDB

## Clinicarx — 2021–2022

Health/pharmacy software. I worked across a newer Laravel/Vue/PostgreSQL surface and legacy CakePHP/AngularJS code.

In one squad I was the senior engineer responsible for architectural direction; in another I spent more time on maintenance and evolution. The work included APIs, PostgreSQL queries/migrations, Vue 3/TypeScript modules and sharing TypeScript practices between squads.

**Used:** Laravel · CakePHP · Vue.js · AngularJS · TypeScript · PostgreSQL

## D7 Med — telemedicine

A telemedicine/video-call product built outside the repositories shown on this account.

I worked on the Vue.js frontend and React application while another developer owned the PHP/PostgreSQL backend. Twilio was used for video, SMS and WhatsApp integrations.

**Used:** Vue.js · React · Twilio · PHP/PostgreSQL integration

## TROC / Monest — 2022

Marketplace work around returns, internal balance/payment flows and performance.

At TROC I worked with Laravel, PostgreSQL, Redis, jQuery and React. At Monest I worked on API evolution and query/performance improvements across NestJS/AdonisJS/MySQL and Laravel/PostgreSQL surfaces.

**Used:** Laravel · PostgreSQL · Redis · React · NestJS · AdonisJS · MySQL

## Teros — 2022

Pricing microservices and architecture work.

My involvement was heavier on prototyping, design and documentation than on day-to-day coding. The system involved C#/Entity Framework/Docker, with Node.js/NestJS and AWS services in the surrounding architecture.

**Used:** C# · Entity Framework · Docker · Node.js/NestJS · AWS

## FCamara / Open Finance — 2022

I worked on internal systems and Open Finance data flows: maintenance, corrections, data preparation for visualizations and technical documentation.

The stack around that work included Node.js, PostgreSQL, MongoDB, Python and Ruby. Pair programming and review were part of the day-to-day work.

**Used:** Node.js · PostgreSQL · MongoDB · Python · Ruby

## Brazilian Outlets / Sarah / Brazipay — 2024–2026

A mix of marketplace, payments, automation and conversational-product work.

The work documented across the period includes maintaining CakePHP/PostgreSQL code, Laravel 10 administrative work, Python/TypeScript automations, a WhatsApp assistant prototype, payment endpoints, tenant migrations, notifications, seeders, project documentation, GitHub Actions and AWS EC2 deployment.

**Used:** PHP · CakePHP · Laravel · PostgreSQL · Python · TypeScript · Docker · GitHub Actions · AWS EC2

## SPRO / NTT — SISAP — 2025–2026

Critical legacy PHP/MySQL work integrated with SAP Business One.

The system had to keep operating while bugs, queries, coupling and new requirements were handled. The documented work includes more than **30 evolutions** across registration/RH flows, validations, documents/reports and integrations.

**Used:** PHP 5.4/5.6 · MySQL 5 · SAP Business One


## Internal / independent work that is not a public repository here

### WhatsApp Service

A Laravel/PHP service designed around asynchronous message ingestion, processing and response rather than a synchronous controller-to-provider flow.

The architecture work includes PostgreSQL, Redis queues/Horizon, idempotency, an outbox, DLQ handling, state-machine rules, Filament/Livewire operations, metrics/SLO thinking and infrastructure automation.

**Used / designed around:** Laravel · PHP · PostgreSQL · Redis · Horizon · Filament · Docker · Prometheus/Grafana · Terraform/Ansible

### DPLMS

An engineering agent/workflow for long codebase audits and refactoring loops.

The interesting part is not "AI writes code". The goal is controlled repetition: find duplication, hardcoded decisions, missing i18n, UI-policy violations, architectural drift, security gaps or useless documentation; fix one class of problem; validate; keep going until the scan stops finding the same category of issue.

I use it as an experiment in machine-readable engineering governance and in making long-running AI work more deterministic.


---

The common thread is less about framework names and more about the kind of system: software that already has users, data, rules and operational risk. I usually prefer to understand what is really there, change it in pieces, add observability and tests around the risky paths, and keep a rollback path.

[← Back to profile](../README.md)
