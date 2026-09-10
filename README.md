# CIRAN Nexus

Build a high-fidelity, modern web application prototype called:

CIRAN

Criminal Intelligence & Relationship Analysis Network

CIRAN is an AI-powered criminal network intelligence and investigation-support platform designed to work as an advanced intelligence layer over existing government criminal-justice systems such as CCTNS/ICJS.

IMPORTANT:

CIRAN does NOT replace existing government systems.

It receives/uses structured investigation data from existing systems and transforms fragmented records into explainable, cross-case, temporal and network-level intelligence.

The prototype must look like a professional law-enforcement intelligence analysis platform, NOT a generic admin dashboard, CRM, banking dashboard, or normal SaaS application.

==================================================

1. DESIGN DIRECTION

==================================================

Create a premium, professional intelligence-command-center UI.

Visual style:

- Dark professional interface

- High readability

- Clean spacing

- Strong visual hierarchy

- Minimal clutter

- Modern cards and panels

- Subtle borders and shadows

- Professional typography

- Data-dense but NOT crowded

- Use restrained accent colors for alerts, intelligence signals and status

- Avoid excessive gradients

- Avoid excessive animations

- Avoid oversized decorative elements

The interface should communicate:

SECURITY + INTELLIGENCE + PRECISION + TRUST

The UI must be extremely easy for an external reviewer to understand within a few seconds.

Every page should clearly communicate:

WHAT is happening?

WHY is it important?

WHAT evidence supports it?

WHAT can the investigator do next?

==================================================

2. GLOBAL LAYOUT

==================================================

Use a consistent application shell:

LEFT SIDEBAR:

- CIRAN logo

- Dashboard

- Investigations

- Network Intelligence

- Cross-Case Analysis

- Timeline

- Intelligence Alerts

- Investigator Copilot

- Evidence & Audit

- Settings

TOP BAR:

- Global search

- Current investigation indicator

- Notifications

- User profile

- Role indicator

MAIN CONTENT:

Responsive content area with clear page titles and contextual actions.

Do NOT create unnecessary pages.

==================================================

3. LOGIN PAGE

==================================================

Create a professional secure login screen.

Brand:

CIRAN

Subtitle:

Criminal Intelligence & Relationship Analysis Network

Fields:

- Officer ID

- Password

Buttons:

- Secure Login

Show a subtle security message:

"Authorized investigation environment"

Do not make it look like a consumer application.

==================================================

4. MAIN DASHBOARD

==================================================

Create a highly informative investigation intelligence dashboard.

Header:

"Intelligence Overview"

Subtitle:

"Unified intelligence from connected investigation records"

Top KPI cards:

1. Active Investigations

2. High-Priority Intelligence Signals

3. Newly Detected Relationships

4. Cross-Case Connections

Main sections:

A. INTELLIGENCE ALERTS

Show realistic mock alerts such as:

"Potential cross-case relationship detected"

"New high-connectivity entity identified"

"Unusual transaction pattern detected"

"Emerging network cluster detected"

Each alert should show:

- Severity

- Timestamp

- Related case

- Short explanation

- View Intelligence button

B. NETWORK ACTIVITY

Show a small network visualization representing:

Persons → Phones → Vehicles → Locations → Cases

C. RECENT INVESTIGATION ACTIVITY

Show:

- Investigation

- Action

- Officer

- Timestamp

D. INTELLIGENCE TREND

Show a clean chart representing detected relationships/patterns over time.

==================================================

5. INVESTIGATION WORKSPACE

==================================================

Create a dedicated investigation workspace.

Header:

"Investigation Workspace"

Search bar:

"Search person, phone, vehicle, case or location..."

Search results should show entity type and relevant information.

When an entity is selected, display:

UNIFIED ENTITY PROFILE

Example:

Name:

Arjun Kumar

Entity Type:

Person

Investigation Priority:

High

Associated Cases:

8

Known Relationships:

14

Recent Activity:

7 events

Then show tabs:

Overview

Network

Timeline

Cases

Evidence

AI Insights

==================================================

6. ENTITY RESOLUTION MODULE

==================================================

Create a screen that demonstrates CIRAN's ability to identify possible duplicate/same entities across fragmented records.

Example:

Record A:

Ravi Kumar

Phone: XXXXX1234

Vehicle: TNXX1234

Record B:

R. Kumar

Phone: XXXXX1234

Vehicle: TNXX1234

AI result:

"POSSIBLE ENTITY MATCH"

Confidence:

92%

Matching attributes:

✓ Phone

✓ Vehicle

✓ Name similarity

Buttons:

- Confirm Match

- Review Evidence

- Reject Match

IMPORTANT:

Never state that the person is definitively the same unless confirmed.

Use "Potential Match", "Possible Association", or "Requires Review".

==================================================

7. NETWORK INTELLIGENCE — HERO SCREEN

==================================================

This is the MOST IMPORTANT screen.

Title:

"Network Intelligence"

Create a large interactive network graph.

Node types:

- Person

- Phone

- Vehicle

- Bank Account

- Location

- Case

Use visually distinguishable node types.

Edges should represent:

- Communication

- Financial transaction

- Shared vehicle

- Shared location

- Case association

Interaction:

When clicking a node:

Open a right-side intelligence panel.

Panel should display:

Entity

Relationship Type

Connected Entity

Source

Timestamp

Confidence

Evidence

Example:

Potential Relationship

Ravi Kumar ↔ Arjun Kumar

Relationship:

Indirect association

Connection path:

Ravi

↓

Kumar

↓

Vehicle TN-XX-1234

↓

Arjun

Confidence:

84%

Supporting Records:

CDR

Vehicle Record

Case Record

Buttons:

"View Evidence"

"Expand Network"

"Analyze Relationship"

The graph should support:

- Zoom

- Pan

- Node selection

- Expand connections

- Filter by relationship type

- Filter by entity type

==================================================

8. TEMPORAL ANALYSIS

==================================================

Create a dedicated timeline intelligence screen.

Title:

"Temporal Analysis"

Display events chronologically.

Example:

JAN 10

Ravi contacts Kumar

JAN 15

Kumar appears at Location A

JAN 18

Financial transaction detected

JAN 22

Case 203 registered

JAN 25

Ravi contacts Kumar again

Allow filters:

- Date range

- Communication

- Financial

- Location

- Case

- Vehicle

Add a feature:

"Detect significant temporal patterns"

Show AI-generated insight:

"Repeated interactions between selected entities were detected around the period of Case 203."

Include:

- Timeline

- Insight

- Supporting evidence

==================================================

9. CROSS-CASE ANALYSIS

==================================================

Create a screen titled:

"Cross-Case Intelligence"

Show multiple investigation cases.

Example:

CASE 101

CASE 156

CASE 203

Display shared entities:

Shared Person

Shared Phone

Shared Vehicle

Shared Location

Shared Associate

Create a visual relationship map connecting cases.

Example:

Case 101

↓

Kumar

↓

Case 156

↓

Ravi

↓

Case 203

Show:

"Potential cross-case relationship detected"

Provide:

- Related cases

- Shared entities

- Relationship path

- Evidence

- Confidence

==================================================

10. HIDDEN PATTERN DETECTION

==================================================

Create an intelligence insights page.

Title:

"Pattern Detection"

Sections:

A. Emerging Network Clusters

B. Indirect Relationships

C. Repeated Entity Associations

D. Unusual Activity Patterns

E. Cross-Case Similarities

Example card:

"Indirect Relationship Detected"

Entities:

Ravi Kumar

Arjun Kumar

Path:

Ravi → Kumar → Vehicle → Arjun

Confidence:

84%

Why it matters:

"This relationship connects entities appearing in separate investigation records."

Buttons:

- Investigate

- View Network

- View Evidence

Do NOT label anyone as "criminal" or "guilty" based solely on AI output.

Use language such as:

"Person of interest"

"Potential association"

"Investigation signal"

"Requires analyst review"

==================================================

11. EXPLAINABLE AI MODULE

==================================================

Create an "AI Intelligence" side panel.

Every AI insight MUST follow this structure:

WHAT WAS DETECTED?

WHY WAS IT DETECTED?

WHAT EVIDENCE SUPPORTS IT?

HOW CONFIDENT IS THE SYSTEM?

WHAT SHOULD THE INVESTIGATOR REVIEW?

Example:

AI Insight

Potential relationship detected between Ravi Kumar and Case 203.

Why?

✓ Shared intermediary

✓ Overlapping location

✓ Related vehicle

✓ Temporal proximity

Confidence:

84%

Evidence:

CDR Record

Vehicle Record

Case Record

Buttons:

"View Source Records"

"Open Network"

"Add to Investigation"

Make this extremely clear and trustworthy.

==================================================

12. INVESTIGATOR COPILOT

==================================================

Create a modern AI investigation assistant.

Title:

"CIRAN Copilot"

Subtitle:

"Ask questions about connected investigation intelligence."

Chat interface.

Example user queries:

"Show all connections between Ravi and Case 203."

"What changed in this network during the last 30 days?"

"Find indirect connections between Ravi and Arjun."

"Which cases share common entities?"

"What evidence supports this relationship?"

AI responses should NOT be plain paragraphs only.

Responses should combine:

- Short explanation

- Relevant entity chips

- Mini graph

- Timeline

- Evidence cards

- Confidence indicator

Example:

QUERY:

Show connections between Ravi and Case 203.

RESULT:

Ravi

↓

Kumar

↓

Vehicle TN-XX-1234

↓

Case 203

Relationship:

Potential indirect association

Confidence:

84%

Evidence:

3 supporting records

[View Network]

[View Evidence]

==================================================

13. EVIDENCE & AUDIT TRAIL

==================================================

Create a dedicated evidence screen.

Title:

"Evidence & Audit"

Every intelligence conclusion must be traceable.

Show:

Insight

Source Record

Record Type

Timestamp

Relationship

Analyst Action

Example:

Insight:

Potential association between Ravi and Arjun

Sources:

CDR-1023

Vehicle-445

Case-203

AI Analysis:

Temporal + relational correlation

Status:

Pending Analyst Review

Include an audit timeline:

Detected

Reviewed

Accepted / Rejected

Analyst Notes

==================================================

14. INTELLIGENCE PRIORITY

==================================================

Create a priority/signal system.

Do NOT call it a "criminal score".

Use:

"Investigation Priority"

or

"Intelligence Priority"

Example:

HIGH

91

Factors:

Cross-case links

Network connectivity

Recent activity

Pattern recurrence

Clearly state:

"Priority score is an investigative signal and does not represent guilt or criminality."

==================================================

15. NOTIFICATION / ALERT CENTER

==================================================

Create an alert center.

Categories:

Critical

High

Medium

Informational

Example alerts:

"New cross-case relationship"

"Emerging network cluster"

"Entity match requires review"

"New anomalous pattern"

"Investigation evidence updated"

Each alert should open the relevant investigation context.

==================================================

16. SETTINGS

==================================================

Keep settings simple.

Sections:

- Profile

- Role

- Notification preferences

- Data access

- Security

- Audit settings

==================================================

17. MOCK DATA

==================================================

Create realistic synthetic/mock data for the prototype.

Use fictional names and fictional records.

Do NOT use real personal data.

Create interconnected sample entities:

Persons:

Ravi Kumar

Arjun Kumar

Karthik Raj

Mohan Das

Priya Shah

Cases:

Case 101

Case 156

Case 203

Case 247

Vehicles:

TN-XX-1234

TN-XX-5678

Locations:

Location A

Location B

Location C

Phones:

XXXX1234

XXXX5678

Bank accounts:

AC-XXXX-102

AC-XXXX-204

Generate relationships across:

- Cases

- Persons

- Phones

- Vehicles

- Locations

- Financial transactions

The data must be consistent across all screens.

==================================================

18. DATA ARCHITECTURE PREPARATION

==================================================

Even though this is primarily a frontend prototype, structure the application so that a backend can easily be connected later.

Use clean reusable components.

Create mock service/API functions for:

getCases()

getEntity()

getNetwork()

getTimeline()

getCrossCaseLinks()

getIntelligenceAlerts()

getEvidence()

askCopilot()

Do NOT hardcode every UI element separately.

Keep data structures modular and replaceable.

==================================================

19. IMPORTANT UX RULES

==================================================

The UI must be:

- Clear

- Professional

- Consistent

- Responsive

- Easy to navigate

- Low clutter

- Investigation-focused

Avoid:

- Excessive cards

- Excessive text

- Giant headings

- Unnecessary animations

- Generic SaaS dashboard appearance

- Fake futuristic graphics

- Overuse of neon effects

Prioritize:

GRAPH

TIMELINE

EVIDENCE

AI INSIGHTS

CROSS-CASE RELATIONSHIPS

==================================================

20. FINAL USER JOURNEY

==================================================

The complete prototype should support this exact journey:

LOGIN

↓

DASHBOARD

↓

SEARCH PERSON

↓

UNIFIED ENTITY PROFILE

↓

NETWORK GRAPH

↓

DISCOVER INDIRECT RELATIONSHIP

↓

TEMPORAL ANALYSIS

↓

CROSS-CASE CONNECTION

↓

EXPLAINABLE AI INSIGHT

↓

VIEW SUPPORTING EVIDENCE

↓

ASK CIRAN COPILOT

↓

INVESTIGATOR DECISION / REVIEW

==================================================

21. MOST IMPORTANT REQUIREMENT

==================================================

The entire application should visually communicate this core concept:

EXISTING GOVERNMENT RECORDS

        ↓

CIRAN INTELLIGENCE LAYER

        ↓

ENTITY RESOLUTION

        ↓

TEMPORAL + CROSS-CASE CORRELATION

        ↓

HIDDEN PATTERN DETECTION

        ↓

EXPLAINABLE AI

        ↓

EVIDENCE-BACKED INVESTIGATIVE INTELLIGENCE

CIRAN should feel like an advanced intelligence-analysis layer on top of existing systems, not another database.

Make the prototype presentation-ready for a Smart India Hackathon external review.

The reviewer should understand the problem, innovation, workflow and investigator value simply by navigating the interface.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/b01da92c-f233-48e4-aed4-b0b42c187dae).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
