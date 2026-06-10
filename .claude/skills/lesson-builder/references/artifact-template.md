# Lesson Artifact Template

A lesson is ONE self-contained HTML file. No build step, no external CDNs.
Inline CSS + vanilla JS only. Below is the required skeleton; fill the
content sections with real teaching material for the specific topic.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{{ADDRESS}} — {{TITLE}}</title>
<style>
  :root { --ink:#1a1a2e; --paper:#fdfdfb; --accent:#2d6a4f; --muted:#6b7280; }
  body { margin:0; font:16px/1.6 system-ui,sans-serif; color:var(--ink);
         background:var(--paper); }
  .wrap { max-width:820px; margin:0 auto; padding:32px 20px 80px; }
  header .addr { font:600 13px ui-monospace,monospace; color:var(--accent);
                 letter-spacing:.05em; }
  h1 { font-size:30px; margin:.2em 0 .1em; }
  .why { color:var(--muted); font-style:italic; margin-bottom:2em; }
  section { margin:2.5em 0; }
  h2 { border-bottom:2px solid var(--accent); padding-bottom:4px; }
  .visual { border:1px solid #e5e7eb; border-radius:12px; padding:16px;
            background:#fff; }
  .q { margin:1.2em 0; padding:14px; border:1px solid #e5e7eb;
       border-radius:10px; }
  .q .opts label { display:block; margin:4px 0; cursor:pointer; }
  button { background:var(--accent); color:#fff; border:0; padding:10px 18px;
           border-radius:8px; font-size:15px; cursor:pointer; }
  #result { margin-top:1em; font-weight:600; }
</style>
</head>
<body>
<div class="wrap">

  <header>
    <div class="addr">{{ADDRESS}}</div>
    <h1>{{TITLE}}</h1>
    <p class="why">{{ONE_LINE_WHY_THIS_MATTERS}}</p>
  </header>

  <!-- 1. WRITTEN / TEACHING SECTION -->
  <section id="learn">
    <h2>Learn</h2>
    <!-- Multiple short subsections at college-course depth: mechanism,
         formulas used (not just named), edge cases, and at least one fully
         worked numeric example. Plain English first, then precise framing.
         Use an engineering/systems analogy where it genuinely clarifies. -->
  </section>

  <!-- 2. VISUAL SECTION(S) — repeat this block, one per mechanism.
       Number the ids (see-1/viz-1, see-2/viz-2, …) to keep them unique.
       Keep the full college-level model; let the interaction (sliders,
       drag handles, live readouts) carry the complexity. -->
  <section id="see-1" class="see">
    <h2>See it: {{MECHANISM_NAME}}</h2>
    <div class="visual" id="viz-1">
      <!-- Inline interactive SVG/Canvas + vanilla JS that SHOWS the concept.
           e.g. draggable curves, animated balances, live-updating chart. -->
    </div>
  </section>

  <!-- 3. QUIZ -->
  <section id="quiz">
    <h2>Check yourself</h2>
    <form id="quizForm">
      <!-- 5-8 questions. Each question element carries data-qid.
           MC options use radio inputs; numeric/text use <input>.
           NEVER mark or hint which option is correct. -->
      <div class="q" data-qid="q1" data-type="mc">
        <p><strong>1.</strong> {{QUESTION_TEXT}}</p>
        <div class="opts">
          <label><input type="radio" name="q1" value="a"> {{OPT_A}}</label>
          <label><input type="radio" name="q1" value="b"> {{OPT_B}}</label>
          <label><input type="radio" name="q1" value="c"> {{OPT_C}}</label>
          <label><input type="radio" name="q1" value="d"> {{OPT_D}}</label>
        </div>
      </div>
      <!-- numeric example -->
      <div class="q" data-qid="q2" data-type="num">
        <p><strong>2.</strong> {{QUESTION_TEXT}}</p>
        <input type="number" name="q2" step="any" />
      </div>

      <button type="submit">Submit answers</button>
    </form>
    <div id="result"></div>
  </section>

</div>

<script>
  // Lesson metadata used by the recorder.
  const LESSON_ADDRESS = "{{ADDRESS}}";

  // Collect answers WITHOUT knowing which are correct. Grading is server-side.
  document.getElementById("quizForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const answers = {};
    document.querySelectorAll(".q").forEach(q => {
      const qid = q.dataset.qid;
      answers[qid] = fd.get(qid);
    });

    const payload = { address: LESSON_ADDRESS, answers, ts: Date.now() };

    try {
      // record_attempt.py (via serve.py) grades against the gated answer key.
      const res = await fetch("http://127.0.0.1:8753/record", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      document.getElementById("result").textContent =
        `Score: ${data.correct}/${data.total}. ` +
        (data.weak_topics?.length ? `Review: ${data.weak_topics.join(", ")}` : "Nice work.");
    } catch (err) {
      // Offline fallback: stash the attempt for later import.
      const blob = new Blob([JSON.stringify(payload, null, 2)],
                            {type:"application/json"});
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `${LESSON_ADDRESS}.attempt.json`;
      a.click();
      document.getElementById("result").textContent =
        "Recorder offline — downloaded attempt JSON. Run scripts/serve.py and import it.";
    }
  });
</script>
</body>
</html>
```

## Rules

- The page never knows the right answers. Only `record_attempt.py` does,
  and only when the approval token exists for that lesson.
- Visuals are vanilla JS + SVG/Canvas. No D3/Chart.js/CDN.
- Multiple "See it" sections are encouraged when the topic has more than one
  mechanism worth isolating — one visual per mechanism beats one overloaded
  visual. See "Depth calibration" in SKILL.md for examples.
- Quiz difficulty mix (from SKILL.md): 1–2 recall, 2–3 application,
  2–3 multi-step computation with realistic numbers.
- Keep each lesson focused on the single topic in its address.
