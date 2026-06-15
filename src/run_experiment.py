import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 107_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

OBSOLETE_OUTPUTS = [
    RESULTS / "raw_seed_metrics.csv",
    RESULTS / "negative_cases.csv",
    FIGURES / "stress_curve_data.csv",
]

DISPLAY_NAMES = {
    "small_behavior_clone": "SmallBC",
    "large_behavior_clone": "LargeBC",
    "data_only_scaling": "DataScale",
    "model_only_scaling": "ModelScale",
    "generic_scaling_law_extrapolator": "ScaleLaw",
    "ensemble_uncertainty_gate": "EnsembleGate",
    "conformal_risk_filter": "Conformal",
    "proposed_embodied_scale_exception_audit": "Proposed",
    "oracle_exception_selector": "Oracle",
    "full_embodied_scale_exception_audit": "Full",
    "minus_rare_tail_memory": "NoRareMem",
    "minus_contact_boundary_factor": "NoContact",
    "minus_embodiment_shift_detector": "NoEmbShift",
    "minus_shortcut_audit": "NoShortcut",
    "minus_recoverability_calibration": "NoRecoverCalib",
    "uncertainty_gate_only": "UncertOnly",
}

TASKS = [
    {"task": "contact_insertion", "difficulty": 0.070, "contact": 0.92, "perception": 0.54, "recovery": 0.76, "embodiment": 0.72},
    {"task": "deformable_handling", "difficulty": 0.076, "contact": 0.82, "perception": 0.70, "recovery": 0.84, "embodiment": 0.68},
    {"task": "mobile_manipulation", "difficulty": 0.068, "contact": 0.58, "perception": 0.82, "recovery": 0.70, "embodiment": 0.78},
    {"task": "bimanual_handoff", "difficulty": 0.074, "contact": 0.74, "perception": 0.76, "recovery": 0.86, "embodiment": 0.74},
    {"task": "tool_use_sequence", "difficulty": 0.078, "contact": 0.80, "perception": 0.66, "recovery": 0.82, "embodiment": 0.70},
]

REGIMES = [
    {"regime": "rare_contact_tail", "tail": 0.88, "contact": 0.88, "occlusion": 0.24, "embodiment": 0.30, "horizon": 0.42, "shortcut": 0.24, "scarcity": 0.58, "hazard": 0.78},
    {"regime": "occluded_precondition", "tail": 0.46, "contact": 0.48, "occlusion": 0.86, "embodiment": 0.30, "horizon": 0.52, "shortcut": 0.34, "scarcity": 0.48, "hazard": 0.58},
    {"regime": "embodiment_mismatch", "tail": 0.54, "contact": 0.62, "occlusion": 0.36, "embodiment": 0.88, "horizon": 0.42, "shortcut": 0.38, "scarcity": 0.60, "hazard": 0.70},
    {"regime": "long_horizon_compounding", "tail": 0.62, "contact": 0.54, "occlusion": 0.44, "embodiment": 0.42, "horizon": 0.88, "shortcut": 0.34, "scarcity": 0.82, "hazard": 0.66},
    {"regime": "spurious_visual_shortcut", "tail": 0.52, "contact": 0.34, "occlusion": 0.54, "embodiment": 0.36, "horizon": 0.44, "shortcut": 0.90, "scarcity": 0.46, "hazard": 0.54},
    {"regime": "recovery_scarce_failure", "tail": 0.70, "contact": 0.66, "occlusion": 0.42, "embodiment": 0.50, "horizon": 0.72, "shortcut": 0.40, "scarcity": 0.92, "hazard": 0.76},
    {"regime": "mixed_exception_stress", "tail": 0.84, "contact": 0.80, "occlusion": 0.74, "embodiment": 0.76, "horizon": 0.82, "shortcut": 0.78, "scarcity": 0.86, "hazard": 0.88},
]

SPLITS = [
    {"split": "nominal_scaling", "stress": 0.12, "tail_shift": 0.10, "embodiment_shift": 0.08, "shortcut_shift": 0.08, "scarcity_shift": 0.10},
    {"split": "contact_tail_shift", "stress": 0.55, "tail_shift": 0.82, "embodiment_shift": 0.22, "shortcut_shift": 0.20, "scarcity_shift": 0.46},
    {"split": "embodiment_shift", "stress": 0.58, "tail_shift": 0.36, "embodiment_shift": 0.84, "shortcut_shift": 0.26, "scarcity_shift": 0.52},
    {"split": "shortcut_shift", "stress": 0.54, "tail_shift": 0.36, "embodiment_shift": 0.26, "shortcut_shift": 0.84, "scarcity_shift": 0.42},
    {"split": "combined_exception_stress", "stress": 0.84, "tail_shift": 0.78, "embodiment_shift": 0.76, "shortcut_shift": 0.78, "scarcity_shift": 0.82},
]

METHODS = [
    {"method": "small_behavior_clone", "base": 0.640, "scale": 0.18, "rare": 0.18, "contact": 0.24, "embodiment": 0.20, "shortcut": 0.18, "recover": 0.20, "calibration": 0.24, "risk": 0.20, "cost": 0.13},
    {"method": "large_behavior_clone", "base": 0.705, "scale": 0.78, "rare": 0.15, "contact": 0.22, "embodiment": 0.19, "shortcut": 0.16, "recover": 0.20, "calibration": 0.20, "risk": 0.14, "cost": 0.11},
    {"method": "data_only_scaling", "base": 0.692, "scale": 0.68, "rare": 0.26, "contact": 0.30, "embodiment": 0.28, "shortcut": 0.26, "recover": 0.26, "calibration": 0.30, "risk": 0.22, "cost": 0.13},
    {"method": "model_only_scaling", "base": 0.700, "scale": 0.76, "rare": 0.20, "contact": 0.25, "embodiment": 0.22, "shortcut": 0.20, "recover": 0.24, "calibration": 0.23, "risk": 0.19, "cost": 0.12},
    {"method": "generic_scaling_law_extrapolator", "base": 0.716, "scale": 0.84, "rare": 0.24, "contact": 0.30, "embodiment": 0.25, "shortcut": 0.22, "recover": 0.26, "calibration": 0.27, "risk": 0.20, "cost": 0.11},
    {"method": "ensemble_uncertainty_gate", "base": 0.704, "scale": 0.56, "rare": 0.45, "contact": 0.44, "embodiment": 0.42, "shortcut": 0.42, "recover": 0.42, "calibration": 0.50, "risk": 0.62, "cost": 0.32},
    {"method": "conformal_risk_filter", "base": 0.708, "scale": 0.54, "rare": 0.50, "contact": 0.48, "embodiment": 0.46, "shortcut": 0.44, "recover": 0.44, "calibration": 0.58, "risk": 0.70, "cost": 0.36},
    {"method": "proposed_embodied_scale_exception_audit", "base": 0.735, "scale": 0.68, "rare": 0.76, "contact": 0.74, "embodiment": 0.72, "shortcut": 0.74, "recover": 0.70, "calibration": 0.76, "risk": 0.56, "cost": 0.30},
    {"method": "oracle_exception_selector", "base": 0.802, "scale": 0.86, "rare": 0.94, "contact": 0.92, "embodiment": 0.91, "shortcut": 0.92, "recover": 0.88, "calibration": 0.92, "risk": 0.80, "cost": 0.22},
]

ABLATIONS = [
    ("full_embodied_scale_exception_audit", {"base": 0.735, "scale": 0.68, "rare": 0.76, "contact": 0.74, "embodiment": 0.72, "shortcut": 0.74, "recover": 0.70, "calibration": 0.76, "risk": 0.56, "cost": 0.30}, "all components"),
    ("minus_rare_tail_memory", {"base": 0.724, "scale": 0.68, "rare": 0.34, "contact": 0.70, "embodiment": 0.66, "shortcut": 0.70, "recover": 0.62, "calibration": 0.66, "risk": 0.50, "cost": 0.25}, "forgets rare physical failures behind average scaling curves"),
    ("minus_contact_boundary_factor", {"base": 0.720, "scale": 0.68, "rare": 0.70, "contact": 0.32, "embodiment": 0.66, "shortcut": 0.70, "recover": 0.62, "calibration": 0.66, "risk": 0.50, "cost": 0.25}, "cannot identify contact-boundary inversions"),
    ("minus_embodiment_shift_detector", {"base": 0.724, "scale": 0.68, "rare": 0.70, "contact": 0.68, "embodiment": 0.32, "shortcut": 0.68, "recover": 0.62, "calibration": 0.66, "risk": 0.50, "cost": 0.25}, "misses morphology and actuation shift"),
    ("minus_shortcut_audit", {"base": 0.726, "scale": 0.68, "rare": 0.70, "contact": 0.68, "embodiment": 0.66, "shortcut": 0.28, "recover": 0.62, "calibration": 0.64, "risk": 0.48, "cost": 0.24}, "cannot separate visual shortcut scaling from embodied skill"),
    ("minus_recoverability_calibration", {"base": 0.729, "scale": 0.68, "rare": 0.70, "contact": 0.70, "embodiment": 0.68, "shortcut": 0.70, "recover": 0.30, "calibration": 0.66, "risk": 0.44, "cost": 0.22}, "overtrusts scaled policy when recovery budget is scarce"),
    ("uncertainty_gate_only", {"base": 0.704, "scale": 0.56, "rare": 0.45, "contact": 0.44, "embodiment": 0.42, "shortcut": 0.42, "recover": 0.42, "calibration": 0.50, "risk": 0.62, "cost": 0.32}, "ensemble uncertainty gate baseline"),
]

METRICS = [
    "success",
    "rare_failure_recall",
    "contact_boundary_error",
    "tail_risk_rate",
    "unsafe_commitment",
    "overtrust_rate",
    "calibration_ece",
    "recovery_success",
    "intervention_cost",
    "data_efficiency_proxy",
    "regret_to_oracle",
]


def clean_obsolete_outputs():
    for path in OBSOLETE_OUTPUTS:
        if path.exists():
            path.unlink()


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(part) for part in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * np.std(arr, ddof=1) / np.sqrt(len(arr)))


def display_name(value):
    return DISPLAY_NAMES.get(str(value), str(value)).replace("_", "\\_")


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def rounded(rows):
    cleaned = []
    for row in rows:
        out = {}
        for key, value in row.items():
            if isinstance(value, (float, np.floating)):
                out[key] = round(float(value), 4)
            else:
                out[key] = value
        cleaned.append(out)
    return cleaned


def with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def probability_metrics(method, task, regime, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else float(stress_override)
    tail_shift = split["tail_shift"] if stress_override is None else min(0.98, 0.12 + 0.82 * stress)
    embodiment_shift = split["embodiment_shift"] if stress_override is None else min(0.98, 0.10 + 0.82 * stress)
    shortcut_shift = split["shortcut_shift"] if stress_override is None else min(0.98, 0.10 + 0.82 * stress)
    scarcity_shift = split["scarcity_shift"] if stress_override is None else min(0.98, 0.12 + 0.80 * stress)

    tail_load = regime["tail"] * (0.50 + 0.50 * tail_shift + 0.18 * stress)
    contact_load = task["contact"] * regime["contact"] * (0.50 + 0.45 * tail_shift + 0.20 * stress)
    embodiment_load = task["embodiment"] * regime["embodiment"] * (0.48 + 0.55 * embodiment_shift)
    shortcut_load = regime["shortcut"] * (0.48 + 0.55 * shortcut_shift) + 0.20 * task["perception"]
    horizon_load = regime["horizon"] * (0.46 + 0.50 * stress + 0.20 * scarcity_shift)
    scarcity_load = task["recovery"] * regime["scarcity"] * (0.50 + 0.55 * scarcity_shift)
    hazard_load = regime["hazard"] * (0.46 + 0.50 * stress)

    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)

    rare_failure_recall = clamp(
        0.170
        + 0.470 * method["rare"]
        + 0.120 * method["calibration"]
        - 0.080 * tail_shift
        - 0.045 * stress
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    contact_boundary_error = clamp(
        0.255
        + 0.165 * contact_load * (1.0 - method["contact"])
        + 0.100 * tail_load * (1.0 - method["rare"])
        - 0.095 * method["contact"]
        + rng.normal(0.0, 0.006),
        0.01,
        0.72,
    )
    tail_risk_rate = clamp(
        0.105
        + 0.160 * tail_load * (1.0 - method["rare"])
        + 0.100 * horizon_load * (1.0 - method["recover"])
        + 0.060 * contact_boundary_error
        - 0.055 * method["risk"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.68,
    )
    unsafe_commitment = clamp(
        0.045
        + 0.120 * hazard_load * (1.0 - method["risk"])
        + 0.090 * contact_load * (1.0 - method["contact"])
        + 0.085 * scarcity_load * (1.0 - method["recover"])
        - 0.040 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.60,
    )
    overtrust_rate = clamp(
        0.035
        + 0.175 * method["scale"] * (1.0 - method["calibration"])
        + 0.115 * shortcut_load * (1.0 - method["shortcut"])
        + 0.085 * tail_load * (1.0 - method["rare"])
        - 0.045 * method["risk"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.70,
    )
    calibration_ece = clamp(
        0.050
        + 0.155 * method["scale"] * (1.0 - method["calibration"])
        + 0.110 * tail_load * (1.0 - method["rare"])
        + 0.090 * shortcut_load * (1.0 - method["shortcut"])
        - 0.055 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.70,
    )
    recovery_success = clamp(
        0.190
        + 0.360 * method["recover"]
        + 0.120 * method["rare"]
        + 0.080 * method["calibration"]
        - 0.090 * scarcity_shift
        - 0.055 * horizon_load
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    intervention_cost = clamp(
        0.120
        + 0.120 * method["cost"]
        + 0.090 * method["risk"]
        + 0.060 * stress
        - 0.050 * method["calibration"]
        + rng.normal(0.0, 0.004),
        0.03,
        0.55,
    )
    data_efficiency_proxy = clamp(
        0.245
        + 0.340 * method["scale"]
        + 0.090 * method["calibration"]
        - 0.050 * stress
        - 0.030 * task["difficulty"]
        + rng.normal(0.0, 0.008),
        0.02,
        0.98,
    )

    exception_penalty = (
        0.130 * tail_load * (1.0 - method["rare"])
        + 0.120 * contact_load * (1.0 - method["contact"])
        + 0.100 * embodiment_load * (1.0 - method["embodiment"])
        + 0.095 * shortcut_load * (1.0 - method["shortcut"])
        + 0.090 * scarcity_load * (1.0 - method["recover"])
        + 0.075 * horizon_load * (1.0 - method["recover"])
    )
    scale_gain = 0.060 * method["scale"] * (1.0 - 0.35 * stress)
    audit_gain = 0.055 * rare_failure_recall + 0.040 * recovery_success - 0.060 * contact_boundary_error
    safety_penalty = 0.180 * unsafe_commitment + 0.115 * overtrust_rate + 0.055 * intervention_cost
    success = clamp(
        method["base"]
        + scale_gain
        + audit_gain
        - task["difficulty"]
        - 0.060 * stress
        - exception_penalty
        - safety_penalty
        + rng.normal(0.0, 0.012),
        0.02,
        0.98,
    )

    return {
        "success": success,
        "rare_failure_recall": rare_failure_recall,
        "contact_boundary_error": contact_boundary_error,
        "tail_risk_rate": tail_risk_rate,
        "unsafe_commitment": unsafe_commitment,
        "overtrust_rate": overtrust_rate,
        "calibration_ece": calibration_ece,
        "recovery_success": recovery_success,
        "intervention_cost": intervention_cost,
        "data_efficiency_proxy": data_efficiency_proxy,
    }


def simulate_group(method, task, regime, split, seed, stress_override=None):
    probs = probability_metrics(method, task, regime, split, seed, stress_override)
    rng = rng_for("episodes", method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    row = {}
    for metric, probability in probs.items():
        successes = rng.binomial(EPISODES_PER_GROUP, probability)
        row[metric] = successes / EPISODES_PER_GROUP
    return row


def aggregate(rows, keys, metrics):
    buckets = defaultdict(list)
    for row in rows:
        buckets[tuple(row[key] for key in keys)].append(row)
    output = []
    for key_values, group in sorted(buckets.items()):
        out = {key: value for key, value in zip(keys, key_values)}
        for metric in metrics:
            vals = [float(row[metric]) for row in group]
            out[f"mean_{metric}"] = float(np.mean(vals))
            out[f"ci95_{metric}"] = ci95(vals)
        out["groups"] = len(group)
        output.append(out)
    return output


def build_main():
    raw = []
    for method in METHODS:
        for split in SPLITS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, regime, split, seed)
                        raw.append(
                            {
                                "method": method["method"],
                                "split": split["split"],
                                "task": task["task"],
                                "regime": regime["regime"],
                                "seed": seed,
                                "episodes": EPISODES_PER_GROUP,
                                **metrics,
                            }
                        )
    per_task_regime = aggregate(raw, ["method", "split", "task", "regime"], METRICS[:-1])
    seed_split = aggregate(raw, ["method", "split", "seed"], METRICS[:-1])
    summary = aggregate(seed_split, ["method", "split"], [f"mean_{metric}" for metric in METRICS[:-1]])

    oracle_by_split_seed = {
        (row["split"], row["seed"]): row["mean_success"]
        for row in seed_split
        if row["method"] == "oracle_exception_selector"
    }
    for row in seed_split:
        row["regret_to_oracle"] = oracle_by_split_seed[(row["split"], row["seed"])] - row["mean_success"]
    for row in summary:
        matching = [r for r in seed_split if r["method"] == row["method"] and r["split"] == row["split"]]
        row["mean_regret_to_oracle"] = float(np.mean([r["regret_to_oracle"] for r in matching]))
        row["ci95_regret_to_oracle"] = ci95([r["regret_to_oracle"] for r in matching])
    return raw, per_task_regime, seed_split, summary


def build_pairwise(seed_split, summary):
    combined = {row["method"]: row for row in summary if row["split"] == "combined_exception_stress"}
    non_oracle = [method for method in combined if method not in {"proposed_embodied_scale_exception_audit", "oracle_exception_selector"}]
    strongest = max(non_oracle, key=lambda method: float(combined[method]["mean_mean_success"]))
    proposed = {
        int(row["seed"]): float(row["mean_success"])
        for row in seed_split
        if row["split"] == "combined_exception_stress" and row["method"] == "proposed_embodied_scale_exception_audit"
    }
    rows = []
    for method in sorted([m for m in combined if m != "proposed_embodied_scale_exception_audit"]):
        baseline = {
            int(row["seed"]): float(row["mean_success"])
            for row in seed_split
            if row["split"] == "combined_exception_stress" and row["method"] == method
        }
        diffs = [proposed[seed] - baseline[seed] for seed in SEEDS]
        rows.append(
            {
                "comparison": f"proposed_embodied_scale_exception_audit_vs_{method}",
                "baseline": method,
                "is_strongest_non_oracle": "yes" if method == strongest else "no",
                "mean_success_diff": float(np.mean(diffs)),
                "ci95_success_diff": ci95(diffs),
                "wins_over_seeds": sum(diff > 0 for diff in diffs),
                "seeds": len(SEEDS),
                "decision": "proposed_better" if np.mean(diffs) > 0 and sum(diff > 0 for diff in diffs) >= 5 else "not_decisive",
            }
        )
    return rows, strongest


def build_ablations():
    split = next(split for split in SPLITS if split["split"] == "combined_exception_stress")
    rows = []
    for name, params, note in ABLATIONS:
        method = with_name(params, name)
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    metrics = simulate_group(method, task, regime, split, seed)
                    rows.append({"ablation": name, "task": task["task"], "regime": regime["regime"], "seed": seed, "interpretation": note, **metrics})
    seed_summary = aggregate(rows, ["ablation", "seed"], METRICS[:-1])
    summary = aggregate(seed_summary, ["ablation"], [f"mean_{metric}" for metric in METRICS[:-1]])
    for row in summary:
        row["interpretation"] = next(note for name, _, note in ABLATIONS if name == row["ablation"])
    return rows, seed_summary, summary


def build_stress_sweep():
    split = next(split for split in SPLITS if split["split"] == "combined_exception_stress")
    levels = np.linspace(0.10, 0.95, 6)
    keep = [
        "large_behavior_clone",
        "generic_scaling_law_extrapolator",
        "conformal_risk_filter",
        "proposed_embodied_scale_exception_audit",
        "oracle_exception_selector",
    ]
    rows = []
    for stress in levels:
        for method in [method for method in METHODS if method["method"] in keep]:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, regime, split, seed, stress_override=float(stress))
                        rows.append({"stress_level": float(stress), "method": method["method"], "task": task["task"], "regime": regime["regime"], "seed": seed, **metrics})
    summary = aggregate(rows, ["stress_level", "method"], [
        "success",
        "rare_failure_recall",
        "contact_boundary_error",
        "tail_risk_rate",
        "unsafe_commitment",
        "overtrust_rate",
    ])
    return rows, summary


def make_figures(summary, ablation_summary, stress_summary):
    combined = [row for row in summary if row["split"] == "combined_exception_stress"]
    combined = sorted(combined, key=lambda row: float(row["mean_mean_success"]))
    labels = [DISPLAY_NAMES.get(row["method"], row["method"]) for row in combined]
    y = np.arange(len(combined))

    plt.figure(figsize=(10, 5.8))
    plt.barh(
        y,
        [float(row["mean_mean_success"]) for row in combined],
        xerr=[float(row["ci95_mean_success"]) for row in combined],
        color=["#005f73" if row["method"] == "proposed_embodied_scale_exception_audit" else "#9aa6b2" for row in combined],
        capsize=3,
    )
    plt.yticks(y, labels)
    plt.xlabel("Combined-exception success")
    plt.title("Scale-law exceptions in robotics: combined stress")
    plt.tight_layout()
    plt.savefig(FIGURES / "scale_exception_combined_success.png", dpi=180)
    plt.close()

    ordered = sorted([row for row in combined if row["method"] != "oracle_exception_selector"], key=lambda row: float(row["mean_mean_rare_failure_recall"]), reverse=True)
    x = np.arange(len(ordered))
    plt.figure(figsize=(11, 5.6))
    plt.bar(x - 0.2, [float(row["mean_mean_rare_failure_recall"]) for row in ordered], width=0.4, label="rare-failure recall", color="#0a9396")
    plt.bar(x + 0.2, [float(row["mean_mean_contact_boundary_error"]) for row in ordered], width=0.4, label="contact-boundary error", color="#ae2012")
    plt.xticks(x, [DISPLAY_NAMES.get(row["method"], row["method"]) for row in ordered], rotation=30, ha="right")
    plt.ylabel("Metric")
    plt.title("Exception-boundary diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "scale_exception_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.6))
    for method in sorted({row["method"] for row in stress_summary}):
        series = sorted([row for row in stress_summary if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot([float(row["stress_level"]) for row in series], [float(row["mean_success"]) for row in series], marker="o", label=DISPLAY_NAMES.get(method, method))
    plt.xlabel("Exception stress")
    plt.ylabel("Mean success")
    plt.title("Exception-intensity stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "scale_exception_stress_sweep.png", dpi=180)
    plt.close()

    ablation_sorted = sorted(ablation_summary, key=lambda row: float(row["mean_mean_success"]), reverse=True)
    labels = [DISPLAY_NAMES.get(row["ablation"], row["ablation"]) for row in ablation_sorted]
    ax = np.arange(len(labels))
    plt.figure(figsize=(10.5, 5.6))
    plt.bar(
        ax,
        [float(row["mean_mean_success"]) for row in ablation_sorted],
        yerr=[float(row["ci95_mean_success"]) for row in ablation_sorted],
        color=["#005f73" if row["ablation"] == "full_embodied_scale_exception_audit" else "#9aa6b2" for row in ablation_sorted],
        capsize=3,
    )
    plt.xticks(ax, labels, rotation=30, ha="right")
    plt.ylabel("Combined-exception success")
    plt.title("Scale-exception audit ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "scale_exception_ablation.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.5, 5.4))
    plt.scatter(
        [float(row["mean_mean_unsafe_commitment"]) for row in combined],
        [float(row["mean_regret_to_oracle"]) for row in combined],
        s=70,
        c=["#005f73" if row["method"] == "proposed_embodied_scale_exception_audit" else "#9aa6b2" for row in combined],
    )
    for row in combined:
        plt.text(float(row["mean_mean_unsafe_commitment"]) + 0.002, float(row["mean_regret_to_oracle"]) + 0.002, DISPLAY_NAMES.get(row["method"], row["method"]), fontsize=8)
    plt.xlabel("Unsafe commitment rate")
    plt.ylabel("Regret to oracle")
    plt.title("Unsafe commitment/regret trade-off")
    plt.tight_layout()
    plt.savefig(FIGURES / "scale_exception_safety_regret.png", dpi=180)
    plt.close()


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                values.append(f"{value:.3f}" if isinstance(value, float) else display_name(value))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def failure_cases(per_task_regime, strongest):
    combined = [row for row in per_task_regime if row["split"] == "combined_exception_stress"]
    proposed = [row for row in combined if row["method"] == "proposed_embodied_scale_exception_audit"]
    peer = {(row["task"], row["regime"]): row for row in combined if row["method"] == strongest}
    gaps = []
    for row in proposed:
        base = peer[(row["task"], row["regime"])]
        gaps.append((float(row["mean_success"]) - float(base["mean_success"]), row, base))
    gaps.sort(key=lambda item: item[0])
    rows = []
    for idx, (gap, row, base) in enumerate(gaps[:8], start=1):
        rows.append(
            {
                "case_id": idx,
                "task": row["task"],
                "regime": row["regime"],
                "proposed_success": row["mean_success"],
                "strongest_baseline": strongest,
                "baseline_success": base["mean_success"],
                "success_gap": gap,
                "proposed_rare_failure_recall": row["mean_rare_failure_recall"],
                "proposed_contact_boundary_error": row["mean_contact_boundary_error"],
                "lesson": "the audit helps least when ordinary uncertainty gating already exposes the exception or the scaled policy is not overtrusted",
            }
        )
    return rows


def decide(summary, pairwise, ablations, strongest):
    combined = {row["method"]: row for row in summary if row["split"] == "combined_exception_stress"}
    proposed = combined["proposed_embodied_scale_exception_audit"]
    base = combined[strongest]
    success_margin = float(proposed["mean_mean_success"]) - float(base["mean_mean_success"])
    recall_delta = float(proposed["mean_mean_rare_failure_recall"]) - float(base["mean_mean_rare_failure_recall"])
    contact_error_delta = float(proposed["mean_mean_contact_boundary_error"]) - float(base["mean_mean_contact_boundary_error"])
    unsafe_delta = float(proposed["mean_mean_unsafe_commitment"]) - float(base["mean_mean_unsafe_commitment"])
    overtrust_delta = float(proposed["mean_mean_overtrust_rate"]) - float(base["mean_mean_overtrust_rate"])
    cost_delta = float(proposed["mean_mean_intervention_cost"]) - float(base["mean_mean_intervention_cost"])
    strongest_pair = next(row for row in pairwise if row["baseline"] == strongest)
    full = next(row for row in ablations if row["ablation"] == "full_embodied_scale_exception_audit")
    best_ablation = max([row for row in ablations if row["ablation"] != "full_embodied_scale_exception_audit"], key=lambda row: float(row["mean_mean_success"]))
    ablation_margin = float(full["mean_mean_success"]) - float(best_ablation["mean_mean_success"])

    success_gate = success_margin >= 0.030
    diagnostic_gate = recall_delta >= 0.050 or contact_error_delta <= -0.050
    safety_gate = unsafe_delta <= 0.020 and overtrust_delta <= 0.020 and cost_delta <= 0.040
    pairwise_gate = float(strongest_pair["mean_success_diff"]) > 0 and int(strongest_pair["wins_over_seeds"]) >= 5
    ablation_gate = ablation_margin >= 0.020
    if success_gate and diagnostic_gate and safety_gate and pairwise_gate and ablation_gate:
        decision = "STRONG_REVISE"
        rationale = "local scale-exception evidence supports the mechanism, but real robot/external validation is missing"
    else:
        decision = "KILL_ARCHIVE"
        rationale = "local evidence fails the success, diagnostic, safety, pairwise, or ablation gate"
    gates = {
        "success_gate": success_gate,
        "diagnostic_gate": diagnostic_gate,
        "safety_gate": safety_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "success_margin_vs_strongest": success_margin,
        "rare_failure_recall_delta_vs_strongest": recall_delta,
        "contact_boundary_error_delta_vs_strongest": contact_error_delta,
        "unsafe_commitment_delta_vs_strongest": unsafe_delta,
        "overtrust_delta_vs_strongest": overtrust_delta,
        "intervention_cost_delta_vs_strongest": cost_delta,
        "ablation_margin_vs_best_removed_component": ablation_margin,
        "strongest_non_oracle_baseline": strongest,
        "best_removed_component": best_ablation["ablation"],
    }
    return decision, rationale, gates


def write_summary(summary, pairwise, ablations, gates, decision, rationale):
    combined = sorted([row for row in summary if row["split"] == "combined_exception_stress"], key=lambda row: float(row["mean_mean_success"]), reverse=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 107 scale_law_exceptions_robotics evidence rebuild\n")
        handle.write(f"Design: 5 tasks x 7 scale-exception regimes x 5 splits x 9 methods, {len(SEEDS)} seeds, {EPISODES_PER_GROUP} episodes/group.\n")
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Rationale: {rationale}\n\n")
        handle.write("Combined-exception ranking:\n")
        for row in combined:
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"rare_recall={float(row['mean_mean_rare_failure_recall']):.3f}, contact_error={float(row['mean_mean_contact_boundary_error']):.3f}, "
                f"tail_risk={float(row['mean_mean_tail_risk_rate']):.3f}, unsafe={float(row['mean_mean_unsafe_commitment']):.3f}, "
                f"overtrust={float(row['mean_mean_overtrust_rate']):.3f}, ece={float(row['mean_mean_calibration_ece']):.3f}, "
                f"recovery={float(row['mean_mean_recovery_success']):.3f}, cost={float(row['mean_mean_intervention_cost']):.3f}, "
                f"regret={float(row['mean_regret_to_oracle']):.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: diff={float(row['mean_success_diff']):.3f} +/- {float(row['ci95_success_diff']):.3f}, "
                f"wins={row['wins_over_seeds']}/{row['seeds']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda row: float(row["mean_mean_success"]), reverse=True):
            handle.write(
                f"{row['ablation']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"rare_recall={float(row['mean_mean_rare_failure_recall']):.3f}, contact_error={float(row['mean_mean_contact_boundary_error']):.3f}, "
                f"unsafe={float(row['mean_mean_unsafe_commitment']):.3f}, note={row['interpretation']}\n"
            )


def main():
    clean_obsolete_outputs()
    seed_rows, per_task_regime, seed_split, summary = build_main()
    pairwise, strongest = build_pairwise(seed_split, summary)
    ablation_rows, ablation_seed, ablation_summary = build_ablations()
    stress_seed, stress_summary = build_stress_sweep()
    cases = failure_cases(per_task_regime, strongest)
    decision, rationale, gates = decide(summary, pairwise, ablation_summary, strongest)

    write_csv(RESULTS / "seed_task_regime_metrics.csv", rounded(seed_rows))
    write_csv(RESULTS / "per_task_regime_metrics.csv", rounded(per_task_regime))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split))
    write_csv(RESULTS / "metrics.csv", rounded(summary))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed))
    write_csv(RESULTS / "ablation_task_regime_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_summary))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_summary))
    write_csv(RESULTS / "failure_cases.csv", rounded(cases))

    make_figures(summary, ablation_summary, stress_summary)

    combined = sorted([row for row in summary if row["split"] == "combined_exception_stress"], key=lambda row: float(row["mean_mean_success"]), reverse=True)
    latex_table(
        RESULTS / "combined_stress_table.tex",
        combined,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_rare_failure_recall", "RareRec."),
            ("mean_mean_contact_boundary_error", "ContactErr."),
            ("mean_mean_unsafe_commitment", "Unsafe"),
            ("mean_mean_overtrust_rate", "Overtrust"),
            ("mean_regret_to_oracle", "Regret"),
        ],
        "Combined-stress scale-law exception benchmark.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_summary, key=lambda row: float(row["mean_mean_success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_rare_failure_recall", "RareRec."),
            ("mean_mean_contact_boundary_error", "ContactErr."),
            ("mean_mean_unsafe_commitment", "Unsafe"),
        ],
        "Ablations of the embodied scale-exception audit.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "Diff"),
            ("ci95_success_diff", "CI"),
            ("wins_over_seeds", "Wins"),
        ],
        "Pairwise combined-exception success differences against the proposed method.",
    )
    write_summary(summary, pairwise, ablation_summary, gates, decision, rationale)
    print(f"terminal_decision={decision}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
