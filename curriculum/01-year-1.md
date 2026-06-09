# Year 1 — Full Courseload with Topic Outlines

This is the heart of the curriculum: a complete first-year business courseload
with every course broken into numbered topics. Each topic is a single lesson
that becomes one HTML artifact (written section + visual section + quiz).

Lesson addressing: `1NN.T` (Year 1, course slot NN, topic T).
When you say *"It's time to work on 105.2,"* that resolves to
**Year 1 → course slot 05 (Managerial Accounting) → topic 2.**

---

## Semester 1

### Course A — `101` Financial Accounting I
*The language of business: how transactions become statements.*

<outline>
- 101.1  Why accounting exists: stakeholders & the accounting equation
- 101.2  The balance sheet: assets, liabilities, equity
- 101.3  The income statement: revenue, expenses, net income
- 101.4  The statement of cash flows (operating/investing/financing)
- 101.5  Double-entry bookkeeping: debits, credits, T-accounts
- 101.6  The accounting cycle: journal → ledger → trial balance
- 101.7  Accrual vs. cash basis; revenue recognition
- 101.8  Adjusting entries: accruals, deferrals, depreciation
- 101.9  Closing the books & preparing financial statements
- 101.10 Reading a real 10-K: tying the four statements together
</outline>

### Course B — `102` Microeconomics
*How individuals and firms make choices under scarcity.*

<outline>
- 102.1  Scarcity, opportunity cost, and the production possibilities frontier
- 102.2  Demand: the curve, shifts, and determinants
- 102.3  Supply: the curve, shifts, and determinants
- 102.4  Market equilibrium and price discovery
- 102.5  Elasticity (price, income, cross) and revenue
- 102.6  Consumer theory: utility and indifference curves
- 102.7  Production and cost in the short and long run
- 102.8  Market structures: perfect competition vs. monopoly
- 102.9  Oligopoly, monopolistic competition, game theory basics
- 102.10 Externalities, public goods, and market failure
</outline>

### Course C — `103` Business Statistics & Data Literacy I
*Describing data and reasoning under uncertainty.*

<outline>
- 103.1  Data types, populations vs. samples, levels of measurement
- 103.2  Descriptive statistics: center, spread, shape
- 103.3  Data visualization: histograms, boxplots, scatterplots
- 103.4  Probability fundamentals and rules
- 103.5  Random variables and expected value
- 103.6  Discrete distributions (binomial, Poisson)
- 103.7  The normal distribution and z-scores
- 103.8  Sampling distributions and the Central Limit Theorem
- 103.9  Confidence intervals: estimating with uncertainty
- 103.10 Intro to correlation and the idea of regression
</outline>

### Course D — `104` Foundations of Management & Organizational Behavior
*How organizations work and how managers lead.*

<outline>
- 104.1  What managers do: planning, organizing, leading, controlling
- 104.2  A short history of management thought
- 104.3  Organizational structure and design
- 104.4  Decision-making models and biases
- 104.5  Motivation theories (Maslow, Herzberg, expectancy)
- 104.6  Leadership styles and contingency models
- 104.7  Teams, group dynamics, and conflict
- 104.8  Organizational culture and change
- 104.9  Corporate governance and stakeholder management
- 104.10 Ethics in management decisions
</outline>

---

## Semester 2

### Course A — `105` Managerial Accounting
*Accounting for internal decision-making.*

<outline>
- 105.1  Financial vs. managerial accounting; the role of cost data
- 105.2  Cost behavior: fixed, variable, mixed
- 105.3  Cost-volume-profit (CVP) analysis and break-even
- 105.4  Job-order costing
- 105.5  Process costing
- 105.6  Activity-based costing (ABC)
- 105.7  Budgeting and the master budget
- 105.8  Standard costs and variance analysis
- 105.9  Relevant costs for decision-making (make-or-buy, special orders)
- 105.10 Capital budgeting basics (payback, NPV preview)
</outline>

### Course B — `106` Macroeconomics
*The aggregate economy and policy levers.*

<outline>
- 106.1  Measuring the economy: GDP and national accounts
- 106.2  Inflation, the CPI, and the cost of living
- 106.3  Unemployment and the labor market
- 106.4  Aggregate demand and aggregate supply
- 106.5  Economic growth and productivity
- 106.6  Money, banking, and the financial system
- 106.7  The central bank and monetary policy
- 106.8  Fiscal policy: spending, taxes, deficits
- 106.9  The business cycle and stabilization
- 106.10 Open-economy macro: trade, exchange rates, balance of payments
</outline>

### Course C — `107` Marketing Principles
*Creating, communicating, and delivering value.*

<outline>
- 107.1  What marketing is: needs, wants, value, exchange
- 107.2  The marketing environment and SWOT
- 107.3  Market research and the marketing information system
- 107.4  Consumer behavior and the buying decision process
- 107.5  Segmentation, targeting, positioning (STP)
- 107.6  Product: the offering, lifecycle, and branding
- 107.7  Price: strategies and psychology
- 107.8  Place: channels and distribution
- 107.9  Promotion: the communication mix
- 107.10 Digital marketing and the modern funnel
</outline>

### Course D — `108` Business Communication & Professional Skills
*Communicating clearly and persuasively in business contexts.*

<outline>
- 108.1  The communication model and audience analysis
- 108.2  Principles of clear business writing
- 108.3  Emails, memos, and short-form business documents
- 108.4  Reports and proposals
- 108.5  Data storytelling and visual communication
- 108.6  Presentations and public speaking
- 108.7  Persuasion and influence (ethos, pathos, logos)
- 108.8  Meetings, negotiation, and difficult conversations
- 108.9  Cross-cultural and remote communication
- 108.10 Personal brand, resumes, and professional networking
</outline>

---

## How this maps to artifacts

Each topic above (e.g. `107.5 Segmentation, targeting, positioning`) becomes
exactly one lesson artifact. The lesson-builder skill (`.claude/skills/lesson-builder`)
defines the artifact structure: a written teaching section, a visual section,
and a quiz whose answer key is gated behind the approval hook.
