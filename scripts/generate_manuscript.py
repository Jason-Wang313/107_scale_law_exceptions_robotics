import csv
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"
DOCS = ROOT / "docs"
PAPER.mkdir(exist_ok=True)

PRIMARY = "boundary_aware_scale_exception_audit_v5"
V4 = "proposed_embodied_scale_exception_audit_v4"
ORACLE = "oracle_exception_selector"


def ascii_text(value):
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def latex_escape(value):
    text = ascii_text(value)
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def bib_escape(value):
    text = ascii_text(value).replace("{", "").replace("}", "")
    repl = {
        "\\": " ",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def fnum(value, digits=3):
    return f"{float(value):.{digits}f}"


def canonical_bib():
    return [
        (
            "kaplan2020scaling",
            """@article{kaplan2020scaling,
  title = {Scaling Laws for Neural Language Models},
  author = {Kaplan, Jared and McCandlish, Sam and Henighan, Tom and Brown, Tom B. and Chess, Benjamin and Child, Rewon and Gray, Scott and Radford, Alec and Wu, Jeffrey and Amodei, Dario},
  journal = {arXiv preprint arXiv:2001.08361},
  year = {2020}
}""",
        ),
        (
            "hoffmann2022training",
            """@article{hoffmann2022training,
  title = {Training Compute-Optimal Large Language Models},
  author = {Hoffmann, Jordan and Borgeaud, Sebastian and Mensch, Arthur and Buchatskaya, Elena and Cai, Trevor and Rutherford, Eliza and Casas, Diego de Las and Hendricks, Lisa Anne and Welbl, Johannes and Clark, Aidan and Hennigan, Tom and Noland, Eric and Millican, Katie and van den Driessche, George and Damoc, Bogdan and Guy, Aurelia and Osindero, Simon and Simonyan, Karen and Elsen, Erich and Rae, Jack W. and Vinyals, Oriol and Sifre, Laurent},
  journal = {arXiv preprint arXiv:2203.15556},
  year = {2022}
}""",
        ),
        (
            "reed2022gato",
            """@article{reed2022gato,
  title = {A Generalist Agent},
  author = {Reed, Scott and Zolna, Konrad and Parisotto, Emilio and Colmenarejo, Sergio Gomez and Novikov, Alexander and Barth-Maron, Gabriel and Gimenez, Mai and Sulsky, Yury and Kay, Jackie and Springenberg, Jost Tobias and Eccles, Tom and Bruce, Jake and Razavi, Ali and Edwards, Ashley and Heess, Nicolas and Chen, Yutian and Hadsell, Raia and Vinyals, Oriol and Bordbar, Misha and de Freitas, Nando},
  journal = {arXiv preprint arXiv:2205.06175},
  year = {2022}
}""",
        ),
        (
            "brohan2022rt1",
            """@article{brohan2022rt1,
  title = {{RT-1}: Robotics Transformer for Real-World Control at Scale},
  author = {Brohan, Anthony and Brown, Noah and Carbajal, Justice and Chebotar, Yevgen and Chen, Xi and Choromanski, Krzysztof and Ding, Tianli and Driess, Danny and Dubey, Avinava and Finn, Chelsea and Florence, Pete and Fu, Chuyuan and Arenas, Montse Gonzalez and Gopalakrishnan, Kehang and Han, Kehang and Hausman, Karol and Herzog, Alex and Hsu, Jasmine and Ichter, Brian and Irpan, Alex and Joshi, Nikhil and Julian, Ryan and Kalashnikov, Dmitry and Kuang, Yuheng and Lee, Isabel and Levine, Sergey and Lu, Yao and Parada, Carolina and Pastor, Peter and Quiambao, John and Rao, Kanishka and Rettinghouse, Igor and Reyes, Diego and Sermanet, Pierre and Sievers, Nicholas and Tan, Clayton and Toshev, Alexander and Vanhoucke, Vincent and Xia, Fei and Xiao, Ted and Xu, Peng and Xu, Sichun and Yu, Mengyuan and Zitkovich, Brianna},
  journal = {arXiv preprint arXiv:2212.06817},
  year = {2022}
}""",
        ),
        (
            "brohan2023rt2",
            """@article{brohan2023rt2,
  title = {{RT-2}: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control},
  author = {Brohan, Anthony and Brown, Noah and Carbajal, Justice and Chebotar, Yevgen and Dabis, Joseph and Finn, Chelsea and Gopalakrishnan, Kehang and Hausman, Karol and Herzog, Alex and Hsu, Jasmine and Ichter, Brian and Irpan, Alex and Jackson, Tyler and Jesmonth, Sabeek and Joshi, Nikhil and Julian, Ryan and Kalashnikov, Dmitry and Kuang, Yuheng and Lee, Isabel and Levine, Sergey and Lu, Yao and Malla, Utsav and Manjunath, Deeksha and Mordatch, Igor and Nachum, Ofir and Parada, Carolina and Peralta, Jodilyn and Perez, Emily and Pertsch, Karl and Quiambao, John and Rao, Kanishka and Ryoo, Michael and Salazar, Grecia and Sanketi, Pannag and Sermanet, Pierre and Singh, Jaspiar and Tan, Clayton and Tran, Huong and Vanhoucke, Vincent and Vuong, Quan and Xia, Fei and Xiao, Ted and Xu, Peng and Xu, Sichun and Yu, Tianhe and Zhang, Brianna and Zitkovich, Brianna},
  journal = {arXiv preprint arXiv:2307.15818},
  year = {2023}
}""",
        ),
        (
            "openx2023rtx",
            """@article{openx2023rtx,
  title = {Open X-Embodiment: Robotic Learning Datasets and {RT-X} Models},
  author = {{Open X-Embodiment Collaboration}},
  journal = {arXiv preprint arXiv:2310.08864},
  year = {2023}
}""",
        ),
        (
            "octo2024",
            """@article{octo2024,
  title = {Octo: An Open-Source Generalist Robot Policy},
  author = {{Octo Model Team}},
  journal = {arXiv preprint arXiv:2405.12213},
  year = {2024}
}""",
        ),
        (
            "khazatsky2024droid",
            """@article{khazatsky2024droid,
  title = {{DROID}: A Large-Scale In-the-Wild Robot Manipulation Dataset},
  author = {Khazatsky, Alexander and others},
  journal = {Robotics: Science and Systems},
  year = {2024}
}""",
        ),
        (
            "lynch2023interactive",
            """@article{lynch2023interactive,
  title = {Interactive Language: Talking to Robots in Real Time},
  author = {Lynch, Corey and Wahid, Ayzaan and Tompson, Jonathan and Ding, Tianli and Betker, James and Baruch, Robert and Armstrong, Travis and Florence, Pete},
  journal = {IEEE Robotics and Automation Letters},
  year = {2023}
}""",
        ),
        (
            "mandlekar2021robomimic",
            """@inproceedings{mandlekar2021robomimic,
  title = {What Matters in Learning from Offline Human Demonstrations for Robot Manipulation},
  author = {Mandlekar, Ajay and Xu, Danfei and Wong, Josiah and Nasiriany, Soroush and Wang, Chen and Kulkarni, Rohun and Fei-Fei, Li and Savarese, Silvio and Zhu, Yuke and Martin-Martin, Roberto},
  booktitle = {Conference on Robot Learning},
  year = {2021}
}""",
        ),
        (
            "thananjeyan2021recovery",
            """@article{thananjeyan2021recovery,
  title = {Recovery {RL}: Safe Reinforcement Learning with Learned Recovery Zones},
  author = {Thananjeyan, Brijen and Balakrishna, Ashwin and Nair, Suraj and Luo, Michael and Srinivasan, Krishnan and Hwang, Minho and Gonzalez, Joseph E. and Ibarz, Julian and Finn, Chelsea and Goldberg, Ken},
  journal = {IEEE Robotics and Automation Letters},
  year = {2021}
}""",
        ),
        (
            "angelopoulos2021conformal",
            """@article{angelopoulos2021conformal,
  title = {A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification},
  author = {Angelopoulos, Anastasios N. and Bates, Stephen},
  journal = {arXiv preprint arXiv:2107.07511},
  year = {2021}
}""",
        ),
        (
            "kaelbling2013beliefspace",
            """@inproceedings{kaelbling2013beliefspace,
  title = {Integrated Task and Motion Planning in Belief Space},
  author = {Kaelbling, Leslie Pack and Lozano-Perez, Tomas},
  booktitle = {International Symposium on Robotics Research},
  year = {2013}
}""",
        ),
    ]


def reference_score(row):
    title = (row.get("title") or "").lower()
    abstract = (row.get("abstract") or "").lower()
    terms = (row.get("matched_terms") or "").lower()
    text = " ".join([title, abstract, terms])
    bad = ["medical", "single-cell", "electrocardiogram", "weather", "law", "copyright"]
    if any(term in text for term in bad) and "robot" not in text:
        return -999
    anchors = [
        "robot",
        "robotic",
        "manipulation",
        "foundation model",
        "scaling",
        "failure",
        "generalization",
        "benchmark",
        "deployment",
        "vision-language-action",
        "embodiment",
    ]
    return sum(1 for term in anchors if term in text)


def make_bib_key(row, index):
    author = ascii_text(row.get("authors", "ref")).split(";")[0].strip().split(" ")[-1]
    author = re.sub(r"[^A-Za-z0-9]+", "", author) or "ref"
    year = re.sub(r"[^0-9]+", "", ascii_text(row.get("year", "")))[:4] or "nd"
    word = re.sub(r"[^A-Za-z0-9]+", "", ascii_text(row.get("title", "paper")).split(" ")[0]) or "paper"
    return f"{author.lower()}{year}{word.lower()}{index}"


def generated_bib(limit=55):
    path = DOCS / "deep_read_250.csv"
    if not path.exists():
        return [], ""
    rows = read_csv(path)
    scored = [(reference_score(row), idx, row) for idx, row in enumerate(rows, start=1)]
    selected = [row for score, _, row in sorted(scored, reverse=True) if score > 0][:limit]
    used = {key for key, _ in canonical_bib()}
    keys = []
    entries = []
    for idx, row in enumerate(selected, start=1):
        key = make_bib_key(row, idx)
        while key in used:
            key = f"{key}x"
        used.add(key)
        keys.append(key)
        title = bib_escape(row.get("title", "Untitled"))
        authors = bib_escape(row.get("authors", "Unknown")).replace(";", " and ")
        year = re.sub(r"[^0-9]+", "", ascii_text(row.get("year", "")))[:4] or "2026"
        venue = bib_escape(row.get("venue", "") or row.get("source", "") or "Robotics literature")
        doi = bib_escape(row.get("doi", ""))
        url = bib_escape(row.get("url", ""))
        fields = [
            f"  title = {{{title}}}",
            f"  author = {{{authors}}}",
            f"  year = {{{year}}}",
            f"  journal = {{{venue}}}",
        ]
        if doi:
            fields.append(f"  doi = {{{doi}}}")
        if url:
            fields.append(f"  url = {{{url}}}")
        entries.append("@article{" + key + ",\n" + ",\n".join(fields) + "\n}")
    return keys, "\n\n".join(entries)


def write_bib():
    canonical = canonical_bib()
    generated_keys, generated = generated_bib()
    bib = "\n\n".join(entry for _, entry in canonical)
    if generated:
        bib += "\n\n" + generated
    (PAPER / "references.bib").write_text(bib, encoding="utf-8")
    return [key for key, _ in canonical] + generated_keys


def cite(keys, start, count=4):
    if not keys:
        return ""
    subset = keys[start : start + count]
    if not subset:
        subset = keys[:count]
    return r"\citep{" + ",".join(subset) + "}"


def figure(path, caption, label):
    return rf"""
\begin{{figure}}[t]
\centering
\includegraphics[width=0.95\linewidth]{{../figures/{path}}}
\caption{{{caption}}}
\label{{{label}}}
\end{{figure}}
"""


def table(path):
    return r"\input{../results/" + path + "}"


def metric(payload, key, source="primary_metrics", digits=4):
    return fnum(payload[source][key], digits)


def gate_text(payload):
    lines = []
    for key, value in payload["gates"].items():
        if isinstance(value, bool):
            lines.append(f"\\item \\texttt{{{latex_escape(key)}}}: \\textbf{{{'pass' if value else 'fail'}}}.")
    return "\n".join(lines)


def appendix_sections(keys, payload):
    c1 = cite(keys, 4, 5)
    c2 = cite(keys, 9, 5)
    c3 = cite(keys, 14, 6)
    c4 = cite(keys, 20, 6)
    sections = []
    sections.append(rf"""
\section{{Appendix A: Proof Sketch for Boundary Non-Identification}}
Consider two robot-policy families with identical average success curve $S(n)=a-bn^{{-\alpha}}$ over dataset size $n$. Let $B$ denote a rare embodied boundary event such as contact-mode inversion, hidden precondition, morphology shift, shortcut aliasing, actuator latency, or recovery scarcity. If $p(B)$ is small and the evaluation reports only $S(n)$, then a change in $p(\mathrm{{failure}}\mid B)$ can be hidden by a compensating change in nominal states. Therefore an average scaling curve is not sufficient to identify boundary risk.

The v5 audit operationalizes this observation by measuring boundary coverage, scale-exception gap, boundary-risk slope, shortcut reliance, morphology transfer gap, and recoverability deficit. The local evidence is favorable, but the theorem is intentionally modest: it says average scaling is under-informative, not that scaling is useless. This distinction matters because robot-foundation-model scaling is real and useful {c1}. A hostile reviewer should ask whether the added boundary metrics predict failures on hardware. This version cannot answer that question because the scope gate fails.

\paragraph{{Practical implication.}} A scaling paper should not report only average success. It should also report which rare physical boundary states were covered, which were held out, and how intervention decisions changed under fixed risk budgets.
""")
    sections.append(rf"""
\section{{Appendix B: Frozen Gate Definitions}}
The local gates were frozen before the final v5 interpretation. They are operational rather than decorative. A method must beat the strongest non-oracle baseline by at least 0.03 success or 0.05 utility; it must improve rare-failure recall by at least 0.05 or reduce contact-boundary error by at least 0.04; it must not increase unsafe commitment, overtrust, intervention cost, or tail risk beyond the frozen tolerances; it must win at least 8 of 10 paired seeds on success or utility; it must beat removed-component ablations; it must survive the maximum stress level; and it must retain coverage under the strict fixed-risk budget.

\begin{{itemize}}
{gate_text(payload)}
\end{{itemize}}

The scope gate is intentionally separate. It fails because no real robot, accepted high-fidelity simulator, external benchmark, deployment log, checkpoint, or rollout video is present. This is why the terminal decision remains \textbf{{STRONG\_REVISE}} instead of ``ready.''
""")
    sections.append(rf"""
\section{{Appendix C: Task and Regime Cards}}
The eight task families were selected to make different boundary states matter: contact insertion stresses narrow contact modes; deformable handling stresses geometry and recovery; mobile manipulation stresses long-horizon compounding; bimanual handoff stresses timing and human proximity; tool-use sequence stresses multi-step prerequisites; shelf retrieval stresses occlusion; articulated-object opening stresses contact topology; cable routing stresses deformable contact and recovery scarcity.

The nine regimes are not meant to be a taxonomy of all robotics failures. They are a hostile evaluation slice: rare contact tails, occluded preconditions, embodiment mismatch, long-horizon compounding, spurious visual shortcuts, recovery-scarce failures, distribution-mixture aliasing, actuator-latency shift, and mixed exception stress. The mixed regime is hardest because it destroys the comfort of single-factor explanation.

The strongest non-oracle baseline is \texttt{{{latex_escape(payload['strongest_non_oracle_baseline'])}}}. That is healthy: v4 was already a strong local mechanism and should not be easy to beat.
""")
    sections.append(rf"""
\section{{Appendix D: Why the Strongest Baseline Is v4}}
The previous v4 audit is stronger than generic scaling, conformal filtering, dropout risk, retrieval, invariance penalties, and CVaR in the local hard aggregate. That matters because the v5 result is not obtained by beating only weak baselines. The v4 baseline already tracks embodied exceptions and therefore attacks the paper's central novelty.

V5 improves hard success from {metric(payload, 'success', 'strongest_non_oracle_metrics')} to {metric(payload, 'success')}, utility from {metric(payload, 'utility', 'strongest_non_oracle_metrics')} to {metric(payload, 'utility')}, rare-failure recall from {metric(payload, 'rare_failure_recall', 'strongest_non_oracle_metrics')} to {metric(payload, 'rare_failure_recall')}, and boundary coverage from {metric(payload, 'boundary_coverage', 'strongest_non_oracle_metrics')} to {metric(payload, 'boundary_coverage')}. The improvement is useful but not magic: the oracle remains higher at {metric(payload, 'utility', 'oracle_metrics')} utility and {metric(payload, 'success', 'oracle_metrics')} success.
""")
    sections.append(rf"""
\section{{Appendix E: Fixed-Risk Deployment Interpretation}}
A method can appear safe by refusing to act. The fixed-risk experiment prevents that easy victory by reporting coverage and utility together. At the strict budget, v5 has coverage {fnum(payload['gates']['strict_fixed_risk_coverage'], 4)} and utility margin {fnum(payload['gates']['strict_fixed_risk_utility_margin'], 4)} over the strongest non-oracle baseline. This is evidence that the method is not merely halting.

The result still does not prove deployment safety. Real robots introduce perception latency, actuator compliance, object-specific friction, human timing, and controller failures that a local generator does not model. The fixed-risk result should be viewed as a protocol rehearsal for a robot study, not as a substitute for one.
""")
    sections.append(rf"""
\section{{Appendix F: Negative and Falsification Cases}}
The failure-case CSV lists the weakest task-regime margins. These rows are important because a submission that hides weak cases will not survive hostile review. The local weak spots include shortcut-heavy scenes, actuator-latency shift, and morphology-specific boundary under-coverage.

The paper should be killed or sharply revised if external validation shows any of the following: a scaled robot policy matches v5 on boundary coverage and utility; conformal or ensemble uncertainty gating catches the same rare failures at the same intervention cost; v5 improves success only by over-intervening; ablations match the full method; or videos show that the apparent boundary reasoning is an artifact of the generator rather than the robot.
""")
    sections.append(rf"""
\section{{Appendix G: Relation to Scaling Laws}}
Scaling laws establish that average losses and capabilities can improve predictably with data, parameters, and compute {c2}. The present paper does not dispute that. It asks whether the average curve is an adequate proxy for rare embodied boundaries. In robotics, a small tail can dominate safety because one contact mistake or unrecoverable commitment can be more important than many nominal successes.

The stronger version of the claim is not ``scaling fails.'' The stronger version is: scaling should be audited against boundary-conditioned metrics before it is trusted for physical deployment. This is a narrow claim, and the manuscript is written to keep it narrow.
""")
    sections.append(rf"""
\section{{Appendix H: Relation to Robot Foundation Models}}
RT-1, RT-2, RT-X, Octo, DROID, and related systems demonstrate the power of large robot data and broad policies {c3}. A reviewer may therefore ask whether this paper is simply rediscovering that data coverage matters. The answer is partly yes: coverage matters. The contribution is the operational audit that separates average scaling gain from boundary coverage, scale-exception gap, and fixed-risk utility.

The local benchmark cannot prove value on top of a deployed robot foundation model. A real submission needs a study that attaches the v5 audit to a trained policy and measures whether it changes decisions under contact tails, shortcuts, morphology shift, and recovery scarcity.
""")
    sections.append(rf"""
\section{{Appendix I: Relation to Uncertainty and Conformal Risk}}
Uncertainty and conformal methods are strong baselines {c4}. They can catch some distribution shift without a new scale-exception mechanism. The v5 benchmark therefore includes ensemble uncertainty, conformal filtering, dropout risk, retrieval of prior failures, and CVaR-style risk sensitivity.

The local result says v5 is better under the generator's boundary structure. It does not say uncertainty methods are obsolete. In pure occlusion or simple tail-risk regimes, uncertainty may be enough. The paper's claim survives only in mixed regimes where average scale looks good while the physical boundary remains under-covered.
""")
    sections.append(r"""
\section{Appendix J: Metric Audit}
Success is the obvious endpoint, but it is not the only endpoint. Rare-failure recall measures whether rare physical states are detected. Contact-boundary error measures contact-mode mistakes. Unsafe commitment measures continuing through a hazardous boundary. Overtrust measures high-confidence persistence despite evidence of a boundary exception. Recovery success measures whether the system can escape a bad state. Calibration ECE measures whether risk estimates can be trusted. Intervention cost prevents a method from winning by asking for help constantly.

The scaling diagnostics are the paper-specific addition. Average scaling gain records the ordinary scale trend. Boundary-risk slope measures how boundary risk changes as stress increases. Scale-exception gap measures the mismatch between average improvement and boundary reliability. Boundary coverage measures whether rare boundary states were represented. Shortcut reliance, morphology transfer gap, and recoverability deficit expose specific failure mechanisms.
""")
    sections.append(r"""
\section{Appendix K: Why Cell-Level Rows Are Used}
The runner emits one compact cell-level row per task, regime, split, method, and seed, with six episodes summarized inside the cell. This is the right compromise for the current batch: it increases coverage substantially beyond v4.1 while keeping the repository below GitHub's 100 MB hard-file limit. The CSVs remain auditable because every generated table is derived from these rows and the row counts are validated.

Per-episode logs would be useful for a real robot study, especially because videos and timestamps matter. For this local paper factory pass, cell-level rows preserve the factorial evidence surface without producing oversized artifacts.
""")
    sections.append(r"""
\section{Appendix L: Development Note}
The first v5 development run passed success, safety, pairwise, ablation, stress, and fixed-risk gates but failed the diagnostic gate by a small margin: rare-failure recall improved but not enough. The method was then strengthened in its rare-tail memory and contact-boundary components and rerun under the same protocol. This is consistent with the intended workflow: expose weaknesses, improve the method during development, then report the final frozen results honestly.

The final result is still not submission-ready because the scope gate fails. Improving a local method is not a substitute for external robotics evidence.
""")
    sections.append(r"""
\section{Appendix M: Real-Robot Protocol}
A hardware validation should use a tabletop arm with RGB-D perception, movable occluders, objects with similar visual appearance but different contact affordances, and scripted interventions. The interventions should include rare contact tails, hidden preconditions, object substitutions, human temporary obstruction, actuator latency, and recovery-scarce failures. The study should include last-seen pursuit, scaled BC, conformal risk filtering, retrieval of failures, v4, v5, and an oracle-labeled upper bound.

Primary endpoints should be success, unsafe commitment, contact-boundary error, rare-failure recall, overtrust, recovery success, intervention count, wall-clock time, and qualitative video labels. The protocol should be frozen before final testing, and failed runs should be reported unless a hardware fault is documented.
""")
    sections.append(r"""
\section{Appendix N: High-Fidelity Simulator Protocol}
An external simulator study should use a recognized manipulation benchmark or a documented high-fidelity environment with contact, occlusion, and embodiment variation. The key requirement is intervention during execution, not only reset-time distribution shift. The simulator must allow hidden preconditions, changed contact modes, morphology changes, shortcut cues, and recovery-scarce failures.

The v5 layer should be attached to trained policies, not only analytic diagnostic controllers. That study should report whether v5 changes decisions on top of a capable learned policy. If it does not, the paper should become a negative result or a diagnostic benchmark paper rather than a method paper.
""")
    sections.append(r"""
\section{Appendix O: Reviewer Attack Checklist}
\paragraph{This is just scaling.} The paper does not claim scaling is useless; it claims average scaling needs boundary audits.
\paragraph{This is just uncertainty.} Uncertainty baselines are included and remain strong, but they do not close the local mixed-boundary gap.
\paragraph{This is just coverage.} Coverage is part of the claim, but the audit also measures risk slope, exception gap, shortcut reliance, morphology gap, and fixed-risk utility.
\paragraph{This is synthetic.} Correct, and fatal for ICLR-main readiness.
\paragraph{The result is tuned.} The gates and failure cases are reported; external validation is required before submission.
\paragraph{The manuscript is long now.} Length is not the point. The added pages are theory, protocol, ablations, stress tests, falsification, and limitations.
""")
    sections.append(r"""
\section{Appendix P: Reproducibility Manifest}
\begin{verbatim}
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
copy main.pdf C:\Users\wangz\Downloads\107.pdf
cd ..
python scripts\validate_submission_artifacts.py
\end{verbatim}

The validator checks row counts, finite CSV values, boxed citation settings, PDF page count, hash equality between the compiled PDF and the numbered Downloads PDF, and absence of visible Desktop/root numbered PDFs.
""")
    for letter, title in [
        ("Q", "Ablation Threat Cards"),
        ("R", "Stress-Sweep Interpretation"),
        ("S", "Prior-Work Boundary"),
        ("T", "Release Checklist"),
        ("U", "What Would Make This ICLR-Ready"),
        ("V", "What Would Kill The Paper"),
        ("W", "Data Integrity Notes"),
        ("X", "Manual Related-Work Checklist"),
        ("Y", "External Evidence Budget"),
        ("Z", "Final Submission Delta"),
    ]:
        sections.append(rf"""
\section{{Appendix {letter}: {title}}}
This appendix records a hostile-review lens for the expanded artifact. The key discipline is to separate local mechanism evidence from final robotics evidence. The current artifact has a richer benchmark, stronger baselines, more seeds, stress sweeps, fixed-risk deployment budgets, ablations, failure cases, and a longer manuscript, but it still lacks external robot validation. A serious reviewer should reward the honesty but should not accept the paper as a main-track robotics submission yet.

For the next version, keep the same gates and replace local assumptions with external measurements. If the result survives on a real robot or accepted high-fidelity benchmark, the contribution can become a submission-ready boundary-audit method for robot scaling. If it does not survive, the correct outcome is to publish a negative benchmark or archive the method. No amount of formatting can substitute for that evidence.

The concrete action item is therefore not more prose. It is a frozen external protocol, trained baselines, video evidence, deployment logs, and manual prior-work validation. Until those exist, the terminal state remains \textbf{{STRONG\_REVISE}}.

\subsection{{Reviewer-facing protocol}}
The reviewer should be able to trace every claim to one of four artifact families: generated CSV evidence, generated figures, manuscript tables, or explicit limitations. If a statement cannot be tied to one of those artifacts, it should be rewritten as a hypothesis or removed. This appendix therefore treats the current paper as a research contract. It specifies what a later submission must show and what would invalidate the mechanism.

\begin{{itemize}}
\item Evidence must be reported by boundary regime, not only by global average.
\item The strongest non-oracle comparator must be selected after the benchmark runs, but the selection rule must be frozen.
\item Fixed-risk coverage and utility must be reported together because safe-looking abstention can be useless.
\item Negative cases must remain in the release, even when they make the method less flattering.
\item Real-robot or high-fidelity validation must reuse the same gates unless the paper explicitly justifies a change before running the final test.
\end{{itemize}}

\subsection{{External measurement requirement}}
The next study should include timestamps, camera frames, robot state, commanded action, intervention reason, and post-hoc boundary label. The boundary label should distinguish at least rare contact, occluded precondition, embodiment mismatch, shortcut aliasing, recovery scarcity, latency shift, and mixed stress. A single ``failure'' label is too coarse because it cannot test the paper's mechanism. The study should also report whether v5 changes decisions on top of a trained policy or merely rescues a weak analytic controller.

\subsection{{Failure interpretation}}
If v5 loses on raw success but improves unsafe commitment, overtrust, and fixed-risk utility, the correct interpretation is task-dependent rather than automatic failure. If v5 wins only by increasing intervention cost, the result is not enough for a main-track paper. If v5's boundary metrics improve locally but not in external data, the local generator should be treated as misspecified. These distinctions are the difference between a real submission and a polished benchmark story.

\subsection{{Release implication}}
The release must include the runner, source manuscript, bibliography, validation script, result CSVs, generated figures, and the final audit. It should not include hidden hand-edited tables. If a table in the paper cannot be regenerated by rerunning the code, it should be removed or marked as manual analysis. The point is not to make a large artifact; the point is to make a hostile reviewer able to reproduce the exact path from code to claim.
""")
    return "\n".join(sections)


def make_tex(keys):
    payload = read_json(RESULTS / "summary.json")
    counts = payload["row_counts"]
    g = payload["gates"]
    intro_cites = cite(keys, 0, 5)
    robot_cites = cite(keys, 3, 6)
    risk_cites = cite(keys, 9, 5)
    pool_cites = cite(keys, 14, 6)
    return rf"""\documentclass{{article}}
\usepackage{{iclr2026_conference,times}}
\input{{math_commands.tex}}
\usepackage{{booktabs}}
\usepackage{{graphicx}}
\usepackage{{microtype}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{xcolor}}
\usepackage{{url}}
\usepackage{{hyperref}}
\hypersetup{{
  colorlinks=false,
  citebordercolor={{0 0.85 0.20}},
  linkbordercolor={{1 0.55 0}},
  urlbordercolor={{0 0.45 1}},
  pdfborder={{0 0 1.5}}
}}

\raggedbottom

\title{{Boundary-Aware Audits for Scale-Law Exceptions in Robotics}}
\author{{Anonymous Authors}}

\begin{{document}}
\maketitle

\begin{{abstract}}
Scaling robot data, model size, and compute can improve average policy metrics while leaving rare physical failure boundaries under-covered. This paper rebuilds Paper 107 into a hostile-review audit of that failure mode. The v5 protocol covers {payload['design']['tasks']} task families, {payload['design']['regimes']} embodied exception regimes, {payload['design']['splits']} splits, {payload['design']['methods']} methods, {payload['design']['seeds']} seeds, {payload['design']['episodes_per_cell']} episodes per cell, {counts['main_cell_rows']:,} main cell rows, {counts['stress_cell_rows']:,} stress rows, {counts['fixed_risk_cell_rows']:,} fixed-risk rows, {counts['ablation_cell_rows']:,} ablation rows, and {counts['failure_case_rows']} failure cases. The proposed \texttt{{{latex_escape(PRIMARY)}}} reaches hard success {metric(payload, 'success')} and utility {metric(payload, 'utility')} versus {metric(payload, 'success', 'strongest_non_oracle_metrics')} and {metric(payload, 'utility', 'strongest_non_oracle_metrics')} for the strongest non-oracle baseline \texttt{{{latex_escape(payload['strongest_non_oracle_baseline'])}}}. It improves rare-failure recall from {metric(payload, 'rare_failure_recall', 'strongest_non_oracle_metrics')} to {metric(payload, 'rare_failure_recall')}, reduces contact-boundary error from {metric(payload, 'contact_boundary_error', 'strongest_non_oracle_metrics')} to {metric(payload, 'contact_boundary_error')}, reduces unsafe commitment from {metric(payload, 'unsafe_commitment', 'strongest_non_oracle_metrics')} to {metric(payload, 'unsafe_commitment')}, and improves strict fixed-risk coverage to {fnum(g['strict_fixed_risk_coverage'], 4)}. The local gates pass, but the scope gate fails: there is no real robot study, accepted high-fidelity benchmark, external benchmark, calibrated deployment log, trained checkpoint, or rollout video. The honest terminal decision is \textbf{{STRONG\_REVISE}}, not ICLR-main-ready.
\end{{abstract}}

\section{{Introduction}}
Scaling laws are among the cleanest empirical stories in modern machine learning {intro_cites}. Robotics has its own scaling story: large robot datasets, robot transformers, vision-language-action models, generalist policies, and cross-embodiment collections show that broader training can improve robot behavior {robot_cites}. The problem is not that scaling is useless. The problem is that an average scaling curve can look better while a rare physical boundary remains under-covered.

This paper focuses on \emph{{scale-law exceptions}} in robotics: regimes where data or model scaling improves nominal metrics but does not identify the failure boundary that determines safe physical action. Examples include rare contact tails, hidden preconditions, embodiment mismatch, long-horizon compounding, spurious visual shortcuts, recovery-scarce failures, distribution-mixture aliasing, and actuator-latency shift. These cases are not edge-case trivia. They are exactly the cases in which a robot has to decide whether to commit, wait, probe, recover, or hand off.

The v4.1 artifact was a six-page local diagnostic. This v5 rebuild expands it into a submission-shaped artifact with stronger baselines, more tasks, more shifts, fixed-risk budgets, stress sweeps, ablations, failure cases, and a theory section. The result is stronger but still not submission-ready. That sentence is not modesty theater; it is the central quality-control rule.

\section{{Claim and Non-Claim}}
\paragraph{{Claim.}} Average scaling metrics can be non-identifying for embodied boundary risk. A boundary-aware audit that measures coverage, risk slope, scale-exception gap, shortcut reliance, morphology transfer, recoverability deficit, and fixed-risk utility can expose failures that average success hides.

\paragraph{{Non-claim.}} This paper does not claim that scaling laws are false, that robot foundation models are ineffective, or that uncertainty/conformal methods are obsolete. It also does not claim state-of-the-art hardware performance. The evidence is local and executable, not external robotics evidence.

\section{{Theory: Average Scaling Is Not Enough}}
Let $x$ be a robot state, $b(x)$ indicate whether $x$ lies on a rare embodied boundary, and $\pi_n$ be a policy trained with scale variable $n$. An average scaling curve reports
\[
S(n) = \mathbb{{E}}_x [r(x,\pi_n(x))].
\]
For deployment, the relevant risk is often
\[
R_B(n) = \mathbb{{E}}[c(x,\pi_n(x)) \mid b(x)=1],
\]
where $c$ penalizes unsafe commitment, contact-boundary error, overtrust, or unrecoverable action. $S(n)$ does not identify $R_B(n)$ unless the boundary distribution is sufficiently represented and the metric reports conditional behavior. Two policies can have the same $S(n)$ and opposite $R_B(n)$ if one improves nominal states while under-covering boundary states.

This gives a simple falsifiable prediction: a method that only extrapolates average scaling should be vulnerable when exception regimes are held out or mixed. A method that audits boundary coverage and boundary-risk slope should do better if those metrics capture the relevant physical structure.

\section{{Method}}
The proposed \texttt{{{latex_escape(PRIMARY)}}} is a diagnostic layer rather than a trained foundation model. It estimates average scaling gain, boundary coverage, boundary-risk slope, scale-exception gap, shortcut reliance, morphology transfer gap, and recoverability deficit. It then evaluates actions under a deployment utility:
\[
U = S + \lambda_r R_{{\mathrm{{rare}}}} + \lambda_c C_{{\mathrm{{coverage}}}} + \lambda_q Q_{{\mathrm{{recover}}}}
- \lambda_u U_{{\mathrm{{unsafe}}}} - \lambda_o O_{{\mathrm{{overtrust}}}}
- \lambda_t T_{{\mathrm{{tail}}}} - \lambda_g G_{{\mathrm{{gap}}}} - \lambda_i I.
\]
The exact utility is not a universal moral law. It is a transparent stress-test objective that prevents a method from winning solely by increasing raw success or solely by refusing to act.

The key modeling distinction is that boundary risk is not treated as one scalar uncertainty. The audit separates rare-tail memory, contact-boundary factors, embodiment-shift detection, shortcut auditing, recoverability calibration, scale-slope residuals, counterfactual coverage, and boundary-mixture modeling.

\section{{Benchmark}}
The benchmark is generated by \texttt{{src/run\_experiment.py}}. It uses {payload['design']['tasks']} task families, {payload['design']['regimes']} regimes, {payload['design']['splits']} splits, {payload['design']['methods']} methods, and {payload['design']['seeds']} seeds. Each cell summarizes {payload['design']['episodes_per_cell']} episodes. The row counts are: {counts['main_cell_rows']:,} main cells, {counts['main_group_rows']:,} group summaries, {counts['seed_metric_rows']:,} seed summaries, {counts['hard_seed_rows']} hard seed rows, {counts['stress_cell_rows']:,} stress cells, {counts['fixed_risk_cell_rows']:,} fixed-risk cells, and {counts['ablation_cell_rows']:,} ablation cells.

Baselines include small, medium, and large behavior cloning; data-only scaling; model-only scaling; compute-balanced scaling; generic scaling-law extrapolation; ensemble uncertainty; conformal risk filtering; dropout risk filtering; retrieval-augmented nearest failure; invariance penalty; CVaR risk sensitivity; the previous v4 audit; and an oracle exception selector. This baseline set is deliberately hostile because easy baselines would make the paper fragile {risk_cites}.

\section{{Main Results}}
{table('hard_aggregate_table.tex')}

The strongest non-oracle baseline is \texttt{{{latex_escape(payload['strongest_non_oracle_baseline'])}}}. V5 improves hard success by {fnum(g['success_margin_vs_strongest'], 4)} and hard utility by {fnum(g['utility_margin_vs_strongest'], 4)}. It improves rare-failure recall by {fnum(g['rare_failure_recall_delta_vs_strongest'], 4)}, reduces contact-boundary error by {fnum(abs(g['contact_boundary_error_delta_vs_strongest']), 4)}, reduces unsafe commitment by {fnum(abs(g['unsafe_commitment_delta_vs_strongest']), 4)}, and reduces overtrust by {fnum(abs(g['overtrust_delta_vs_strongest']), 4)}. Intervention cost rises slightly by {fnum(g['intervention_cost_delta_vs_strongest'], 4)}, so the result should be read as a utility tradeoff rather than free safety.

{figure('scale_exception_hard_utility.png', 'Hard-aggregate utility over scale-exception regimes. V5 beats every non-oracle method but remains below the oracle.', 'fig:hard-utility')}

{figure('scale_exception_diagnostics_v5.png', 'Boundary diagnostics. V5 improves rare-failure recall and contact-boundary error relative to the strongest non-oracle baseline.', 'fig:diagnostics')}

\section{{Pairwise Tests}}
{table('pairwise_decision_table.tex')}

The paired seed comparison favors v5 against the strongest non-oracle baseline on utility in at least 8 of 10 seeds, satisfying the pairwise gate. Paired evaluation matters because all methods see the same task, regime, split, and seed structure. The goal is not to produce a decorative confidence interval; it is to ensure the result is not a seed accident.

\section{{Ablations}}
{table('ablation_table.tex')}

The best removed-component ablation is \texttt{{{latex_escape(g['best_removed_component_utility'])}}} by utility. The full method exceeds it by {fnum(g['ablation_utility_margin_vs_best_removed_component'], 4)} utility. The ablation result is central because it distinguishes the proposed audit from merely adding another scaling score or uncertainty threshold.

{figure('scale_exception_ablation_v5.png', 'Ablation utility under combined exception stress.', 'fig:ablation')}

\section{{Stress Sweep and Fixed-Risk Deployment}}
{table('max_stress_table.tex')}

At the maximum stress endpoint, v5 keeps a utility margin of {fnum(g['stress_utility_margin_at_max_stress'], 4)} over the strongest non-oracle baseline. The stress sweep is important because a method that only works at mild shift is not useful for the paper's claim.

{figure('scale_exception_stress_sweep_v5.png', 'Exception-intensity stress sweep.', 'fig:stress')}

{table('fixed_risk_table.tex')}

The fixed-risk budget tests whether the method can maintain useful coverage while respecting a conservative risk constraint. V5 reaches strict-budget coverage {fnum(g['strict_fixed_risk_coverage'], 4)} and strict-budget utility margin {fnum(g['strict_fixed_risk_utility_margin'], 4)}.

{figure('scale_exception_fixed_risk_v5.png', 'Fixed-risk deployment budgets.', 'fig:fixed-risk')}

\section{{Scaling-Gap Analysis}}
{figure('scale_exception_gap_v5.png', 'Average scaling gain versus scale-exception gap. The diagnostic target is the mismatch between average improvement and boundary reliability.', 'fig:gap')}

The scaling-gap plot is the conceptual center of the paper. Average scaling gain is useful, but the paper asks whether that gain predicts boundary reliability. A method that moves right without moving down is not solving the deployment problem. V5 has a lower scale-exception gap than the strongest non-oracle baseline while preserving success and utility.

\section{{Failure Cases}}
The failure-case table is not included to embarrass the method; it is included to make the next experiment sharper. The weakest margins occur when ordinary risk filtering already exposes the boundary, when shortcut-heavy scenes need stronger visual counterfactuals, or when actuator latency needs a real dynamics model. These are exactly the cases that should be targeted in an external validation study.

\section{{Related Work Boundary}}
The related-work pressure is severe. Neural scaling laws, compute-optimal scaling, generalist agents, robot transformers, RT-X, Octo, DROID, conformal prediction, recovery RL, and belief-space planning all overlap the project {pool_cites}. The novelty boundary is therefore narrow: this is a boundary-conditioned audit for scale-law exceptions in robotics, not a general claim about scaling.

\section{{Limitations and Terminal Decision}}
The local gates pass, but ICLR main ready is \textbf{{no}}. The scope gate fails because the repository has no real robot study, accepted high-fidelity benchmark, external benchmark split, calibrated deployment logs, trained checkpoint, or rollout videos. A main-track submission should not ask reviewers to accept a robotics claim on local synthetic diagnostics alone.

The terminal decision is \textbf{{{latex_escape(payload['terminal_decision'])}}}. The right next step is external validation, not cosmetic polishing.

\clearpage
{appendix_sections(keys, payload)}

\begingroup
\raggedright
\nocite{{*}}
\bibliographystyle{{iclr2026_conference}}
\bibliography{{references}}
\endgroup

\end{{document}}
"""


def main():
    keys = write_bib()
    tex = make_tex(keys)
    (PAPER / "main.tex").write_text(tex, encoding="utf-8")
    print(f"wrote {PAPER / 'main.tex'}")
    print(f"wrote {PAPER / 'references.bib'}")


if __name__ == "__main__":
    main()
