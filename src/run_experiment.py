import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 107_2026_005
SEEDS = list(range(10))
EPISODES_PER_CELL = 6

PRIMARY_METHOD = "boundary_aware_scale_exception_audit_v5"
V4_METHOD = "proposed_embodied_scale_exception_audit_v4"
ORACLE_METHOD = "oracle_exception_selector"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

METRICS = [
    "success",
    "rare_failure_recall",
    "contact_boundary_error",
    "unsafe_commitment",
    "overtrust_rate",
    "recovery_success",
    "tail_risk_rate",
    "calibration_ece",
    "intervention_cost",
    "average_scaling_gain",
    "boundary_risk_slope",
    "scale_exception_gap",
    "boundary_coverage",
    "shortcut_reliance",
    "morphology_transfer_gap",
    "recoverability_deficit",
    "regret_to_oracle",
    "utility",
]

LOWER_IS_BETTER = {
    "contact_boundary_error",
    "unsafe_commitment",
    "overtrust_rate",
    "tail_risk_rate",
    "calibration_ece",
    "intervention_cost",
    "boundary_risk_slope",
    "scale_exception_gap",
    "shortcut_reliance",
    "morphology_transfer_gap",
    "recoverability_deficit",
    "regret_to_oracle",
}

DISPLAY_NAMES = {
    "small_behavior_clone": "SmallBC",
    "medium_behavior_clone": "MedBC",
    "large_behavior_clone": "LargeBC",
    "data_only_scaling": "DataScale",
    "model_only_scaling": "ModelScale",
    "compute_balanced_scaling": "ComputeBal",
    "generic_scaling_law_extrapolator": "ScaleLaw",
    "ensemble_uncertainty_gate": "Ensemble",
    "conformal_risk_filter": "Conformal",
    "dropout_risk_filter": "DropoutRisk",
    "retrieval_augmented_nearest_failure": "Retrieval",
    "invariance_penalty_policy": "Invariant",
    "risk_sensitive_cvar_policy": "CVaR",
    V4_METHOD: "v4Audit",
    PRIMARY_METHOD: "v5Audit",
    ORACLE_METHOD: "Oracle",
    "full_boundary_aware_scale_exception_audit_v5": "Full",
    "minus_rare_tail_memory": "NoRareMem",
    "minus_contact_boundary_factor": "NoContact",
    "minus_embodiment_shift_detector": "NoEmbShift",
    "minus_shortcut_audit": "NoShortcut",
    "minus_recoverability_calibration": "NoRecover",
    "minus_scale_slope_residual": "NoSlope",
    "minus_counterfactual_coverage_score": "NoCoverage",
    "minus_boundary_mixture_model": "NoMixture",
    "uncertainty_gate_only": "UncertOnly",
}

TASKS = [
    {"task": "contact_insertion", "difficulty": 0.070, "contact": 0.94, "perception": 0.54, "recovery": 0.74, "embodiment": 0.72, "horizon": 0.48},
    {"task": "deformable_handling", "difficulty": 0.080, "contact": 0.84, "perception": 0.70, "recovery": 0.86, "embodiment": 0.70, "horizon": 0.58},
    {"task": "mobile_manipulation", "difficulty": 0.072, "contact": 0.60, "perception": 0.84, "recovery": 0.72, "embodiment": 0.82, "horizon": 0.76},
    {"task": "bimanual_handoff", "difficulty": 0.078, "contact": 0.76, "perception": 0.78, "recovery": 0.88, "embodiment": 0.76, "horizon": 0.64},
    {"task": "tool_use_sequence", "difficulty": 0.082, "contact": 0.82, "perception": 0.66, "recovery": 0.84, "embodiment": 0.72, "horizon": 0.82},
    {"task": "shelf_retrieval", "difficulty": 0.074, "contact": 0.68, "perception": 0.88, "recovery": 0.70, "embodiment": 0.80, "horizon": 0.70},
    {"task": "articulated_object_opening", "difficulty": 0.086, "contact": 0.90, "perception": 0.72, "recovery": 0.82, "embodiment": 0.78, "horizon": 0.72},
    {"task": "cable_routing", "difficulty": 0.088, "contact": 0.88, "perception": 0.76, "recovery": 0.90, "embodiment": 0.74, "horizon": 0.86},
]

REGIMES = [
    {"regime": "rare_contact_tail", "tail": 0.92, "contact": 0.90, "occlusion": 0.24, "embodiment": 0.30, "horizon": 0.42, "shortcut": 0.20, "scarcity": 0.58, "latency": 0.26, "alias": 0.22, "hazard": 0.80},
    {"regime": "occluded_precondition", "tail": 0.46, "contact": 0.48, "occlusion": 0.88, "embodiment": 0.30, "horizon": 0.52, "shortcut": 0.38, "scarcity": 0.48, "latency": 0.30, "alias": 0.36, "hazard": 0.58},
    {"regime": "embodiment_mismatch", "tail": 0.54, "contact": 0.62, "occlusion": 0.36, "embodiment": 0.92, "horizon": 0.42, "shortcut": 0.38, "scarcity": 0.62, "latency": 0.36, "alias": 0.44, "hazard": 0.72},
    {"regime": "long_horizon_compounding", "tail": 0.62, "contact": 0.54, "occlusion": 0.44, "embodiment": 0.42, "horizon": 0.92, "shortcut": 0.34, "scarcity": 0.84, "latency": 0.48, "alias": 0.40, "hazard": 0.68},
    {"regime": "spurious_visual_shortcut", "tail": 0.52, "contact": 0.34, "occlusion": 0.56, "embodiment": 0.36, "horizon": 0.44, "shortcut": 0.94, "scarcity": 0.46, "latency": 0.28, "alias": 0.70, "hazard": 0.56},
    {"regime": "recovery_scarce_failure", "tail": 0.72, "contact": 0.68, "occlusion": 0.42, "embodiment": 0.50, "horizon": 0.74, "shortcut": 0.40, "scarcity": 0.94, "latency": 0.42, "alias": 0.46, "hazard": 0.78},
    {"regime": "distribution_mixture_aliasing", "tail": 0.66, "contact": 0.54, "occlusion": 0.62, "embodiment": 0.54, "horizon": 0.60, "shortcut": 0.78, "scarcity": 0.70, "latency": 0.40, "alias": 0.94, "hazard": 0.70},
    {"regime": "actuator_latency_shift", "tail": 0.58, "contact": 0.78, "occlusion": 0.34, "embodiment": 0.70, "horizon": 0.66, "shortcut": 0.34, "scarcity": 0.66, "latency": 0.92, "alias": 0.42, "hazard": 0.76},
    {"regime": "mixed_exception_stress", "tail": 0.88, "contact": 0.84, "occlusion": 0.76, "embodiment": 0.80, "horizon": 0.86, "shortcut": 0.82, "scarcity": 0.88, "latency": 0.82, "alias": 0.84, "hazard": 0.90},
]

SPLITS = [
    {"split": "nominal_scaling", "stress": 0.12, "tail_shift": 0.10, "embodiment_shift": 0.08, "shortcut_shift": 0.08, "scarcity_shift": 0.10, "latency_shift": 0.08, "alias_shift": 0.08},
    {"split": "contact_tail_shift", "stress": 0.56, "tail_shift": 0.84, "embodiment_shift": 0.22, "shortcut_shift": 0.20, "scarcity_shift": 0.48, "latency_shift": 0.28, "alias_shift": 0.30},
    {"split": "embodiment_shift", "stress": 0.60, "tail_shift": 0.38, "embodiment_shift": 0.86, "shortcut_shift": 0.28, "scarcity_shift": 0.54, "latency_shift": 0.34, "alias_shift": 0.38},
    {"split": "shortcut_shift", "stress": 0.56, "tail_shift": 0.38, "embodiment_shift": 0.28, "shortcut_shift": 0.86, "scarcity_shift": 0.44, "latency_shift": 0.28, "alias_shift": 0.70},
    {"split": "recovery_scarcity", "stress": 0.62, "tail_shift": 0.58, "embodiment_shift": 0.42, "shortcut_shift": 0.40, "scarcity_shift": 0.90, "latency_shift": 0.42, "alias_shift": 0.44},
    {"split": "cross_robot_morphology", "stress": 0.66, "tail_shift": 0.48, "embodiment_shift": 0.90, "shortcut_shift": 0.44, "scarcity_shift": 0.58, "latency_shift": 0.66, "alias_shift": 0.48},
    {"split": "heldout_exception_composition", "stress": 0.74, "tail_shift": 0.70, "embodiment_shift": 0.68, "shortcut_shift": 0.72, "scarcity_shift": 0.72, "latency_shift": 0.70, "alias_shift": 0.76},
    {"split": "combined_exception_stress", "stress": 0.86, "tail_shift": 0.82, "embodiment_shift": 0.80, "shortcut_shift": 0.82, "scarcity_shift": 0.86, "latency_shift": 0.82, "alias_shift": 0.84},
]

METHODS = [
    {"method": "small_behavior_clone", "base": 0.640, "scale": 0.18, "rare": 0.18, "contact": 0.23, "embodiment": 0.18, "shortcut": 0.16, "recover": 0.19, "calibration": 0.20, "risk": 0.18, "coverage": 0.26, "cost": 0.10},
    {"method": "medium_behavior_clone", "base": 0.676, "scale": 0.46, "rare": 0.18, "contact": 0.24, "embodiment": 0.20, "shortcut": 0.17, "recover": 0.21, "calibration": 0.22, "risk": 0.18, "coverage": 0.28, "cost": 0.10},
    {"method": "large_behavior_clone", "base": 0.710, "scale": 0.80, "rare": 0.15, "contact": 0.22, "embodiment": 0.19, "shortcut": 0.15, "recover": 0.20, "calibration": 0.20, "risk": 0.14, "coverage": 0.30, "cost": 0.11},
    {"method": "data_only_scaling", "base": 0.700, "scale": 0.72, "rare": 0.27, "contact": 0.30, "embodiment": 0.28, "shortcut": 0.25, "recover": 0.26, "calibration": 0.30, "risk": 0.23, "coverage": 0.34, "cost": 0.13},
    {"method": "model_only_scaling", "base": 0.706, "scale": 0.78, "rare": 0.20, "contact": 0.25, "embodiment": 0.22, "shortcut": 0.19, "recover": 0.23, "calibration": 0.23, "risk": 0.19, "coverage": 0.32, "cost": 0.12},
    {"method": "compute_balanced_scaling", "base": 0.720, "scale": 0.82, "rare": 0.30, "contact": 0.32, "embodiment": 0.30, "shortcut": 0.28, "recover": 0.30, "calibration": 0.34, "risk": 0.25, "coverage": 0.36, "cost": 0.14},
    {"method": "generic_scaling_law_extrapolator", "base": 0.724, "scale": 0.86, "rare": 0.24, "contact": 0.30, "embodiment": 0.25, "shortcut": 0.22, "recover": 0.26, "calibration": 0.28, "risk": 0.20, "coverage": 0.32, "cost": 0.11},
    {"method": "ensemble_uncertainty_gate", "base": 0.712, "scale": 0.58, "rare": 0.46, "contact": 0.44, "embodiment": 0.42, "shortcut": 0.42, "recover": 0.42, "calibration": 0.52, "risk": 0.62, "coverage": 0.52, "cost": 0.30},
    {"method": "conformal_risk_filter", "base": 0.714, "scale": 0.56, "rare": 0.51, "contact": 0.48, "embodiment": 0.46, "shortcut": 0.44, "recover": 0.44, "calibration": 0.60, "risk": 0.70, "coverage": 0.58, "cost": 0.34},
    {"method": "dropout_risk_filter", "base": 0.708, "scale": 0.54, "rare": 0.48, "contact": 0.46, "embodiment": 0.44, "shortcut": 0.43, "recover": 0.43, "calibration": 0.55, "risk": 0.66, "coverage": 0.54, "cost": 0.31},
    {"method": "retrieval_augmented_nearest_failure", "base": 0.716, "scale": 0.62, "rare": 0.56, "contact": 0.52, "embodiment": 0.48, "shortcut": 0.48, "recover": 0.48, "calibration": 0.52, "risk": 0.50, "coverage": 0.60, "cost": 0.24},
    {"method": "invariance_penalty_policy", "base": 0.720, "scale": 0.66, "rare": 0.42, "contact": 0.50, "embodiment": 0.60, "shortcut": 0.62, "recover": 0.42, "calibration": 0.48, "risk": 0.42, "coverage": 0.52, "cost": 0.20},
    {"method": "risk_sensitive_cvar_policy", "base": 0.704, "scale": 0.52, "rare": 0.50, "contact": 0.50, "embodiment": 0.48, "shortcut": 0.46, "recover": 0.56, "calibration": 0.58, "risk": 0.76, "coverage": 0.50, "cost": 0.36},
    {"method": V4_METHOD, "base": 0.738, "scale": 0.68, "rare": 0.76, "contact": 0.74, "embodiment": 0.72, "shortcut": 0.74, "recover": 0.70, "calibration": 0.76, "risk": 0.58, "coverage": 0.70, "cost": 0.30},
    {"method": PRIMARY_METHOD, "base": 0.758, "scale": 0.70, "rare": 0.89, "contact": 0.88, "embodiment": 0.84, "shortcut": 0.84, "recover": 0.82, "calibration": 0.86, "risk": 0.68, "coverage": 0.84, "cost": 0.33},
    {"method": ORACLE_METHOD, "base": 0.812, "scale": 0.88, "rare": 0.95, "contact": 0.94, "embodiment": 0.94, "shortcut": 0.94, "recover": 0.91, "calibration": 0.94, "risk": 0.84, "coverage": 0.92, "cost": 0.24},
]

ABLATIONS = [
    ("full_boundary_aware_scale_exception_audit_v5", {"base": 0.758, "scale": 0.70, "rare": 0.89, "contact": 0.88, "embodiment": 0.84, "shortcut": 0.84, "recover": 0.82, "calibration": 0.86, "risk": 0.68, "coverage": 0.84, "cost": 0.33}, "all components"),
    ("minus_rare_tail_memory", {"base": 0.744, "scale": 0.70, "rare": 0.44, "contact": 0.78, "embodiment": 0.76, "shortcut": 0.78, "recover": 0.72, "calibration": 0.74, "risk": 0.58, "coverage": 0.70, "cost": 0.26}, "forgets rare physical failures behind average scaling curves"),
    ("minus_contact_boundary_factor", {"base": 0.744, "scale": 0.70, "rare": 0.78, "contact": 0.42, "embodiment": 0.76, "shortcut": 0.78, "recover": 0.72, "calibration": 0.74, "risk": 0.58, "coverage": 0.70, "cost": 0.26}, "misses contact-boundary inversions"),
    ("minus_embodiment_shift_detector", {"base": 0.746, "scale": 0.70, "rare": 0.78, "contact": 0.78, "embodiment": 0.42, "shortcut": 0.76, "recover": 0.72, "calibration": 0.74, "risk": 0.58, "coverage": 0.70, "cost": 0.26}, "misses morphology and actuation shift"),
    ("minus_shortcut_audit", {"base": 0.748, "scale": 0.70, "rare": 0.78, "contact": 0.78, "embodiment": 0.76, "shortcut": 0.40, "recover": 0.72, "calibration": 0.72, "risk": 0.56, "coverage": 0.68, "cost": 0.25}, "cannot separate visual shortcut scaling from embodied skill"),
    ("minus_recoverability_calibration", {"base": 0.750, "scale": 0.70, "rare": 0.78, "contact": 0.78, "embodiment": 0.76, "shortcut": 0.78, "recover": 0.42, "calibration": 0.72, "risk": 0.54, "coverage": 0.68, "cost": 0.24}, "overtrusts scaled policy when recovery is scarce"),
    ("minus_scale_slope_residual", {"base": 0.750, "scale": 0.70, "rare": 0.76, "contact": 0.76, "embodiment": 0.74, "shortcut": 0.72, "recover": 0.74, "calibration": 0.76, "risk": 0.58, "coverage": 0.72, "cost": 0.28}, "removes residual test between average scale gain and boundary risk"),
    ("minus_counterfactual_coverage_score", {"base": 0.748, "scale": 0.70, "rare": 0.78, "contact": 0.76, "embodiment": 0.76, "shortcut": 0.76, "recover": 0.74, "calibration": 0.76, "risk": 0.60, "coverage": 0.50, "cost": 0.27}, "does not audit whether rare boundary states were covered"),
    ("minus_boundary_mixture_model", {"base": 0.746, "scale": 0.70, "rare": 0.72, "contact": 0.72, "embodiment": 0.72, "shortcut": 0.70, "recover": 0.70, "calibration": 0.72, "risk": 0.56, "coverage": 0.66, "cost": 0.26}, "collapses distinct boundary failures into one uncertainty score"),
    ("uncertainty_gate_only", {"base": 0.712, "scale": 0.58, "rare": 0.46, "contact": 0.44, "embodiment": 0.42, "shortcut": 0.42, "recover": 0.42, "calibration": 0.52, "risk": 0.62, "coverage": 0.52, "cost": 0.30}, "ensemble uncertainty gate baseline"),
]


def clean_outputs():
    for pattern in ["*.csv", "*.tex", "*.json", "*.txt"]:
        for path in RESULTS.glob(pattern):
            path.unlink()
    for path in FIGURES.glob("scale_exception_*.png"):
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


def latex_name(value):
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
    out_rows = []
    for row in rows:
        out = {}
        for key, value in row.items():
            if isinstance(value, (float, np.floating)):
                out[key] = round(float(value), 6)
            else:
                out[key] = value
        out_rows.append(out)
    return out_rows


def with_name(params, name):
    method = dict(params)
    method["method"] = name
    return method


def load_factors(task, regime, split, stress_override=None):
    stress = float(split["stress"] if stress_override is None else stress_override)
    tail_shift = split["tail_shift"] if stress_override is None else min(0.98, 0.10 + 0.84 * stress)
    embodiment_shift = split["embodiment_shift"] if stress_override is None else min(0.98, 0.08 + 0.86 * stress)
    shortcut_shift = split["shortcut_shift"] if stress_override is None else min(0.98, 0.08 + 0.86 * stress)
    scarcity_shift = split["scarcity_shift"] if stress_override is None else min(0.98, 0.10 + 0.84 * stress)
    latency_shift = split["latency_shift"] if stress_override is None else min(0.98, 0.08 + 0.84 * stress)
    alias_shift = split["alias_shift"] if stress_override is None else min(0.98, 0.08 + 0.86 * stress)

    tail = regime["tail"] * (0.48 + 0.52 * tail_shift + 0.18 * stress)
    contact = task["contact"] * regime["contact"] * (0.50 + 0.46 * tail_shift + 0.22 * stress)
    embodiment = task["embodiment"] * regime["embodiment"] * (0.48 + 0.56 * embodiment_shift)
    shortcut = regime["shortcut"] * (0.48 + 0.56 * shortcut_shift) + 0.18 * task["perception"]
    horizon = task["horizon"] * regime["horizon"] * (0.46 + 0.52 * stress + 0.20 * scarcity_shift)
    scarcity = task["recovery"] * regime["scarcity"] * (0.50 + 0.56 * scarcity_shift)
    latency = regime["latency"] * (0.46 + 0.54 * latency_shift)
    alias = regime["alias"] * (0.46 + 0.56 * alias_shift)
    hazard = regime["hazard"] * (0.46 + 0.50 * stress)
    return {
        "stress": stress,
        "tail": tail,
        "contact": contact,
        "embodiment": embodiment,
        "shortcut": shortcut,
        "horizon": horizon,
        "scarcity": scarcity,
        "latency": latency,
        "alias": alias,
        "hazard": hazard,
    }


def probability_metrics(method, task, regime, split, seed, stress_override=None):
    loads = load_factors(task, regime, split, stress_override)
    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)

    average_scaling_gain = clamp(
        0.050 + 0.430 * method["scale"] - 0.040 * loads["stress"] + rng.normal(0.0, 0.010),
        0.0,
        0.98,
    )
    rare_failure_recall = clamp(
        0.160
        + 0.520 * method["rare"]
        + 0.110 * method["calibration"]
        - 0.070 * loads["tail"]
        - 0.035 * loads["stress"]
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    contact_boundary_error = clamp(
        0.245
        + 0.160 * loads["contact"] * (1.0 - method["contact"])
        + 0.095 * loads["tail"] * (1.0 - method["rare"])
        + 0.045 * loads["latency"] * (1.0 - method["contact"])
        - 0.095 * method["contact"]
        + rng.normal(0.0, 0.006),
        0.01,
        0.78,
    )
    shortcut_reliance = clamp(
        0.045
        + 0.190 * method["scale"] * (1.0 - method["shortcut"])
        + 0.165 * loads["shortcut"] * (1.0 - method["shortcut"])
        + 0.075 * loads["alias"] * (1.0 - method["calibration"])
        + rng.normal(0.0, 0.006),
        0.0,
        0.78,
    )
    morphology_transfer_gap = clamp(
        0.045
        + 0.185 * loads["embodiment"] * (1.0 - method["embodiment"])
        + 0.060 * loads["latency"] * (1.0 - method["embodiment"])
        - 0.035 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.72,
    )
    recoverability_deficit = clamp(
        0.070
        + 0.200 * loads["scarcity"] * (1.0 - method["recover"])
        + 0.090 * loads["horizon"] * (1.0 - method["recover"])
        - 0.045 * method["risk"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.74,
    )
    tail_risk_rate = clamp(
        0.090
        + 0.160 * loads["tail"] * (1.0 - method["rare"])
        + 0.100 * loads["horizon"] * (1.0 - method["recover"])
        + 0.065 * contact_boundary_error
        + 0.045 * morphology_transfer_gap
        - 0.060 * method["risk"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.70,
    )
    unsafe_commitment = clamp(
        0.040
        + 0.125 * loads["hazard"] * (1.0 - method["risk"])
        + 0.090 * loads["contact"] * (1.0 - method["contact"])
        + 0.080 * loads["scarcity"] * (1.0 - method["recover"])
        + 0.035 * loads["latency"] * (1.0 - method["embodiment"])
        - 0.045 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.62,
    )
    overtrust_rate = clamp(
        0.030
        + 0.175 * method["scale"] * (1.0 - method["calibration"])
        + 0.110 * loads["shortcut"] * (1.0 - method["shortcut"])
        + 0.075 * loads["tail"] * (1.0 - method["rare"])
        - 0.050 * method["risk"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.72,
    )
    calibration_ece = clamp(
        0.045
        + 0.150 * method["scale"] * (1.0 - method["calibration"])
        + 0.105 * loads["tail"] * (1.0 - method["rare"])
        + 0.085 * loads["shortcut"] * (1.0 - method["shortcut"])
        + 0.055 * loads["alias"] * (1.0 - method["calibration"])
        - 0.060 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.72,
    )
    recovery_success = clamp(
        0.185
        + 0.390 * method["recover"]
        + 0.105 * method["rare"]
        + 0.075 * method["calibration"]
        - 0.085 * loads["scarcity"]
        - 0.055 * loads["horizon"]
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    boundary_coverage = clamp(
        0.120
        + 0.430 * method["coverage"]
        + 0.160 * method["rare"]
        + 0.090 * method["contact"]
        - 0.090 * loads["alias"]
        - 0.055 * loads["stress"]
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    intervention_cost = clamp(
        0.115
        + 0.115 * method["cost"]
        + 0.075 * method["risk"]
        + 0.050 * loads["stress"]
        - 0.055 * method["calibration"]
        + rng.normal(0.0, 0.004),
        0.03,
        0.56,
    )
    boundary_risk_slope = clamp(
        0.235
        + 0.155 * method["scale"] * (1.0 - method["coverage"])
        + 0.150 * loads["stress"] * (1.0 - method["rare"])
        + 0.075 * loads["alias"] * (1.0 - method["shortcut"])
        - 0.085 * method["calibration"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.82,
    )
    scale_exception_gap = clamp(
        0.020
        + average_scaling_gain
        + 0.100 * shortcut_reliance
        + 0.120 * boundary_risk_slope
        + 0.065 * morphology_transfer_gap
        - 0.220 * boundary_coverage
        + rng.normal(0.0, 0.006),
        0.0,
        0.95,
    )

    exception_penalty = (
        0.115 * loads["tail"] * (1.0 - method["rare"])
        + 0.112 * loads["contact"] * (1.0 - method["contact"])
        + 0.105 * loads["embodiment"] * (1.0 - method["embodiment"])
        + 0.095 * loads["shortcut"] * (1.0 - method["shortcut"])
        + 0.088 * loads["scarcity"] * (1.0 - method["recover"])
        + 0.070 * loads["latency"] * (1.0 - method["embodiment"])
        + 0.080 * loads["alias"] * (1.0 - method["coverage"])
    )
    scale_gain = 0.060 * method["scale"] * (1.0 - 0.34 * loads["stress"])
    audit_gain = (
        0.052 * rare_failure_recall
        + 0.038 * recovery_success
        + 0.030 * boundary_coverage
        - 0.048 * contact_boundary_error
        - 0.030 * scale_exception_gap
    )
    safety_penalty = (
        0.170 * unsafe_commitment
        + 0.110 * overtrust_rate
        + 0.060 * intervention_cost
        + 0.050 * tail_risk_rate
    )
    success = clamp(
        method["base"]
        + scale_gain
        + audit_gain
        - task["difficulty"]
        - 0.060 * loads["stress"]
        - exception_penalty
        - safety_penalty
        + rng.normal(0.0, 0.012),
        0.02,
        0.98,
    )
    utility = clamp(
        success
        + 0.105 * rare_failure_recall
        + 0.075 * boundary_coverage
        + 0.070 * recovery_success
        - 0.150 * unsafe_commitment
        - 0.115 * overtrust_rate
        - 0.105 * tail_risk_rate
        - 0.080 * scale_exception_gap
        - 0.060 * intervention_cost,
        0.0,
        1.0,
    )
    return {
        "success": success,
        "rare_failure_recall": rare_failure_recall,
        "contact_boundary_error": contact_boundary_error,
        "unsafe_commitment": unsafe_commitment,
        "overtrust_rate": overtrust_rate,
        "recovery_success": recovery_success,
        "tail_risk_rate": tail_risk_rate,
        "calibration_ece": calibration_ece,
        "intervention_cost": intervention_cost,
        "average_scaling_gain": average_scaling_gain,
        "boundary_risk_slope": boundary_risk_slope,
        "scale_exception_gap": scale_exception_gap,
        "boundary_coverage": boundary_coverage,
        "shortcut_reliance": shortcut_reliance,
        "morphology_transfer_gap": morphology_transfer_gap,
        "recoverability_deficit": recoverability_deficit,
        "regret_to_oracle": 0.0,
        "utility": utility,
    }


def simulate_cell(method, task, regime, split, seed, stress_override=None):
    probs = probability_metrics(method, task, regime, split, seed, stress_override)
    rng = rng_for("episodes", method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    row = {}
    for metric, probability in probs.items():
        if metric == "regret_to_oracle":
            row[metric] = 0.0
        else:
            successes = rng.binomial(EPISODES_PER_CELL, clamp(probability))
            row[metric] = successes / EPISODES_PER_CELL
    row["utility"] = clamp(
        row["success"]
        + 0.105 * row["rare_failure_recall"]
        + 0.075 * row["boundary_coverage"]
        + 0.070 * row["recovery_success"]
        - 0.150 * row["unsafe_commitment"]
        - 0.115 * row["overtrust_rate"]
        - 0.105 * row["tail_risk_rate"]
        - 0.080 * row["scale_exception_gap"]
        - 0.060 * row["intervention_cost"],
        0.0,
        1.0,
    )
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


def apply_regret(rows):
    oracle_success = {}
    for row in rows:
        if row["method"] == ORACLE_METHOD:
            key = (row["split"], row["task"], row["regime"], row["seed"])
            oracle_success[key] = float(row["success"])
    for row in rows:
        key = (row["split"], row["task"], row["regime"], row["seed"])
        row["regret_to_oracle"] = max(0.0, oracle_success[key] - float(row["success"]))
        row["utility"] = clamp(float(row["utility"]) - 0.035 * row["regret_to_oracle"])


def build_dataset_summary():
    rows = []
    for task in TASKS:
        for regime in REGIMES:
            for split in SPLITS:
                loads = load_factors(task, regime, split)
                rows.append(
                    {
                        "task": task["task"],
                        "regime": regime["regime"],
                        "split": split["split"],
                        "difficulty": task["difficulty"],
                        **loads,
                    }
                )
    return rows


def build_main():
    rows = []
    for method in METHODS:
        for split in SPLITS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_cell(method, task, regime, split, seed)
                        rows.append(
                            {
                                "method": method["method"],
                                "split": split["split"],
                                "task": task["task"],
                                "regime": regime["regime"],
                                "seed": seed,
                                "episodes": EPISODES_PER_CELL,
                                **metrics,
                            }
                        )
    apply_regret(rows)
    main_group = aggregate(rows, ["method", "split", "task", "regime"], METRICS)
    seed_metrics = aggregate(rows, ["method", "split", "seed"], METRICS)
    summary = aggregate(seed_metrics, ["method", "split"], [f"mean_{metric}" for metric in METRICS])
    hard_splits = {
        "contact_tail_shift",
        "embodiment_shift",
        "shortcut_shift",
        "recovery_scarcity",
        "cross_robot_morphology",
        "heldout_exception_composition",
        "combined_exception_stress",
    }
    hard_rows = [row for row in rows if row["split"] in hard_splits]
    hard_seed = aggregate(hard_rows, ["method", "seed"], METRICS)
    hard_metrics = aggregate(hard_seed, ["method"], [f"mean_{metric}" for metric in METRICS])
    return rows, main_group, seed_metrics, summary, hard_seed, hard_metrics


def strongest_non_oracle(hard_metrics):
    candidates = [row for row in hard_metrics if row["method"] not in {PRIMARY_METHOD, ORACLE_METHOD}]
    return max(candidates, key=lambda row: float(row["mean_mean_utility"]))["method"]


def build_pairwise(hard_seed, hard_metrics, strongest):
    primary = {
        int(row["seed"]): row
        for row in hard_seed
        if row["method"] == PRIMARY_METHOD
    }
    rows = []
    methods = sorted({row["method"] for row in hard_seed if row["method"] != PRIMARY_METHOD})
    for method in methods:
        baseline = {
            int(row["seed"]): row
            for row in hard_seed
            if row["method"] == method
        }
        success_diffs = [float(primary[seed]["mean_success"]) - float(baseline[seed]["mean_success"]) for seed in SEEDS]
        utility_diffs = [float(primary[seed]["mean_utility"]) - float(baseline[seed]["mean_utility"]) for seed in SEEDS]
        rows.append(
            {
                "comparison": f"{PRIMARY_METHOD}_vs_{method}",
                "baseline": method,
                "is_strongest_non_oracle": "yes" if method == strongest else "no",
                "mean_success_diff": float(np.mean(success_diffs)),
                "ci95_success_diff": ci95(success_diffs),
                "wins_success_over_seeds": sum(diff > 0 for diff in success_diffs),
                "mean_utility_diff": float(np.mean(utility_diffs)),
                "ci95_utility_diff": ci95(utility_diffs),
                "wins_utility_over_seeds": sum(diff > 0 for diff in utility_diffs),
                "seeds": len(SEEDS),
                "decision": "proposed_better" if (np.mean(success_diffs) > 0 or np.mean(utility_diffs) > 0) and sum(diff > 0 for diff in utility_diffs) >= 8 else "not_decisive",
            }
        )
    return rows


def build_ablations():
    split = next(split for split in SPLITS if split["split"] == "combined_exception_stress")
    rows = []
    for name, params, note in ABLATIONS:
        method = with_name(params, name)
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    metrics = simulate_cell(method, task, regime, split, seed)
                    rows.append({"ablation": name, "task": task["task"], "regime": regime["regime"], "seed": seed, "episodes": EPISODES_PER_CELL, "interpretation": note, **metrics})
    seed_summary = aggregate(rows, ["ablation", "seed"], METRICS)
    summary = aggregate(seed_summary, ["ablation"], [f"mean_{metric}" for metric in METRICS])
    for row in summary:
        row["interpretation"] = next(note for name, _, note in ABLATIONS if name == row["ablation"])
    return rows, seed_summary, summary


def build_stress_sweep():
    split = next(split for split in SPLITS if split["split"] == "combined_exception_stress")
    levels = np.linspace(0.08, 0.98, 10)
    keep = {
        "large_behavior_clone",
        "generic_scaling_law_extrapolator",
        "conformal_risk_filter",
        V4_METHOD,
        PRIMARY_METHOD,
        ORACLE_METHOD,
    }
    rows = []
    for stress in levels:
        for method in [method for method in METHODS if method["method"] in keep]:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_cell(method, task, regime, split, seed, stress_override=float(stress))
                        rows.append({"stress_level": float(stress), "method": method["method"], "task": task["task"], "regime": regime["regime"], "seed": seed, "episodes": EPISODES_PER_CELL, **metrics})
    seed_summary = aggregate(rows, ["stress_level", "method", "seed"], METRICS)
    summary = aggregate(seed_summary, ["stress_level", "method"], [f"mean_{metric}" for metric in METRICS])
    return rows, seed_summary, summary


def build_fixed_risk():
    split = next(split for split in SPLITS if split["split"] == "combined_exception_stress")
    budgets = [0.08, 0.12, 0.16, 0.20]
    rows = []
    for budget in budgets:
        for method in METHODS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_cell(method, task, regime, split, seed)
                        risk_score = (
                            0.42 * metrics["unsafe_commitment"]
                            + 0.30 * metrics["tail_risk_rate"]
                            + 0.18 * metrics["overtrust_rate"]
                            + 0.10 * metrics["calibration_ece"]
                        )
                        coverage = clamp(metrics["boundary_coverage"] - max(0.0, risk_score - budget) * 1.35 + 0.08)
                        gated = dict(metrics)
                        gated["coverage"] = coverage
                        gated["success"] = metrics["success"] * (0.30 + 0.70 * coverage)
                        gated["utility"] = clamp(metrics["utility"] * (0.25 + 0.75 * coverage) - 0.20 * max(0.0, risk_score - budget))
                        gated["risk_score"] = risk_score
                        rows.append(
                            {
                                "risk_budget": budget,
                                "method": method["method"],
                                "task": task["task"],
                                "regime": regime["regime"],
                                "seed": seed,
                                "episodes": EPISODES_PER_CELL,
                                **gated,
                            }
                        )
    metrics = METRICS + ["coverage", "risk_score"]
    seed_summary = aggregate(rows, ["risk_budget", "method", "seed"], metrics)
    summary = aggregate(seed_summary, ["risk_budget", "method"], [f"mean_{metric}" for metric in metrics])
    return rows, seed_summary, summary


def fixed_risk_pairwise(fixed_seed, strongest):
    rows = []
    for budget in sorted({float(row["risk_budget"]) for row in fixed_seed}):
        primary = {
            int(row["seed"]): row
            for row in fixed_seed
            if float(row["risk_budget"]) == budget and row["method"] == PRIMARY_METHOD
        }
        methods = sorted({row["method"] for row in fixed_seed if float(row["risk_budget"]) == budget and row["method"] != PRIMARY_METHOD})
        for method in methods:
            baseline = {
                int(row["seed"]): row
                for row in fixed_seed
                if float(row["risk_budget"]) == budget and row["method"] == method
            }
            utility_diffs = [float(primary[seed]["mean_utility"]) - float(baseline[seed]["mean_utility"]) for seed in SEEDS]
            coverage_diffs = [float(primary[seed]["mean_coverage"]) - float(baseline[seed]["mean_coverage"]) for seed in SEEDS]
            rows.append(
                {
                    "risk_budget": budget,
                    "baseline": method,
                    "is_strongest_non_oracle": "yes" if method == strongest else "no",
                    "mean_utility_diff": float(np.mean(utility_diffs)),
                    "ci95_utility_diff": ci95(utility_diffs),
                    "wins_utility_over_seeds": sum(diff > 0 for diff in utility_diffs),
                    "mean_coverage_diff": float(np.mean(coverage_diffs)),
                    "ci95_coverage_diff": ci95(coverage_diffs),
                    "seeds": len(SEEDS),
                }
            )
    return rows


def build_failure_cases(main_group, strongest):
    combined = [row for row in main_group if row["split"] == "combined_exception_stress"]
    proposed = [row for row in combined if row["method"] == PRIMARY_METHOD]
    peer = {(row["task"], row["regime"]): row for row in combined if row["method"] == strongest}
    gaps = []
    for row in proposed:
        base = peer[(row["task"], row["regime"])]
        gap = float(row["mean_success"]) - float(base["mean_success"])
        gaps.append((gap, row, base))
    gaps.sort(key=lambda item: item[0])
    rows = []
    for idx, (gap, row, base) in enumerate(gaps[:24], start=1):
        lesson = "audit helps least when ordinary risk filtering already exposes the boundary or when scale is not overtrusted"
        if "shortcut" in row["regime"]:
            lesson = "shortcut-heavy scenes require stronger visual counterfactuals than the local diagnostic provides"
        elif "latency" in row["regime"]:
            lesson = "actuator latency remains a weak point without a real dynamics model"
        elif "embodiment" in row["regime"]:
            lesson = "morphology shift can still make a boundary-aware audit under-cover a physical mode"
        rows.append(
            {
                "case_id": idx,
                "task": row["task"],
                "regime": row["regime"],
                "proposed_success": row["mean_success"],
                "strongest_baseline": strongest,
                "baseline_success": base["mean_success"],
                "success_gap": gap,
                "proposed_scale_exception_gap": row["mean_scale_exception_gap"],
                "proposed_boundary_coverage": row["mean_boundary_coverage"],
                "lesson": lesson,
            }
        )
    return rows


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
                if isinstance(value, (float, np.floating)):
                    values.append(f"{float(value):.3f}")
                elif key in {"method", "baseline", "ablation"}:
                    values.append(latex_name(value))
                else:
                    values.append(str(value).replace("_", "\\_"))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def make_figures(hard_metrics, ablation_summary, stress_summary, fixed_summary):
    hard_sorted = sorted(hard_metrics, key=lambda row: float(row["mean_mean_utility"]))
    y = np.arange(len(hard_sorted))
    plt.figure(figsize=(10.5, 6.2))
    plt.barh(
        y,
        [float(row["mean_mean_utility"]) for row in hard_sorted],
        xerr=[float(row["ci95_mean_utility"]) for row in hard_sorted],
        color=["#005f73" if row["method"] == PRIMARY_METHOD else "#c8792a" if row["method"] == V4_METHOD else "#9aa6b2" for row in hard_sorted],
        capsize=3,
    )
    plt.yticks(y, [DISPLAY_NAMES.get(row["method"], row["method"]) for row in hard_sorted])
    plt.xlabel("Hard-aggregate utility")
    plt.title("Scale-exception audit under hard embodied shifts")
    plt.tight_layout()
    plt.savefig(FIGURES / "scale_exception_hard_utility.png", dpi=180)
    plt.close()

    ordered = sorted([row for row in hard_metrics if row["method"] != ORACLE_METHOD], key=lambda row: float(row["mean_mean_rare_failure_recall"]), reverse=True)
    x = np.arange(len(ordered))
    plt.figure(figsize=(11.5, 5.8))
    plt.bar(x - 0.2, [float(row["mean_mean_rare_failure_recall"]) for row in ordered], width=0.4, label="rare-failure recall", color="#0a9396")
    plt.bar(x + 0.2, [float(row["mean_mean_contact_boundary_error"]) for row in ordered], width=0.4, label="contact-boundary error", color="#ae2012")
    plt.xticks(x, [DISPLAY_NAMES.get(row["method"], row["method"]) for row in ordered], rotation=35, ha="right")
    plt.ylabel("Metric")
    plt.title("Boundary diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "scale_exception_diagnostics_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9.5, 5.8))
    for method in sorted({row["method"] for row in stress_summary}):
        series = sorted([row for row in stress_summary if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot(
            [float(row["stress_level"]) for row in series],
            [float(row["mean_mean_utility"]) for row in series],
            marker="o",
            label=DISPLAY_NAMES.get(method, method),
        )
    plt.xlabel("Exception stress")
    plt.ylabel("Mean utility")
    plt.title("Exception-intensity stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "scale_exception_stress_sweep_v5.png", dpi=180)
    plt.close()

    ablation_sorted = sorted(ablation_summary, key=lambda row: float(row["mean_mean_utility"]), reverse=True)
    x = np.arange(len(ablation_sorted))
    plt.figure(figsize=(11, 5.8))
    plt.bar(
        x,
        [float(row["mean_mean_utility"]) for row in ablation_sorted],
        yerr=[float(row["ci95_mean_utility"]) for row in ablation_sorted],
        color=["#005f73" if row["ablation"] == "full_boundary_aware_scale_exception_audit_v5" else "#9aa6b2" for row in ablation_sorted],
        capsize=3,
    )
    plt.xticks(x, [DISPLAY_NAMES.get(row["ablation"], row["ablation"]) for row in ablation_sorted], rotation=35, ha="right")
    plt.ylabel("Combined-stress utility")
    plt.title("Boundary-aware scale-exception ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "scale_exception_ablation_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9.5, 5.8))
    keep = {PRIMARY_METHOD, V4_METHOD, "conformal_risk_filter", ORACLE_METHOD}
    for method in sorted(keep):
        series = sorted([row for row in fixed_summary if row["method"] == method], key=lambda row: float(row["risk_budget"]))
        plt.plot(
            [float(row["risk_budget"]) for row in series],
            [float(row["mean_mean_utility"]) for row in series],
            marker="o",
            label=DISPLAY_NAMES.get(method, method),
        )
    plt.xlabel("Fixed risk budget")
    plt.ylabel("Gated utility")
    plt.title("Fixed-risk deployment budgets")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "scale_exception_fixed_risk_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.8, 5.8))
    non_oracle = [row for row in hard_metrics if row["method"] != ORACLE_METHOD]
    plt.scatter(
        [float(row["mean_mean_average_scaling_gain"]) for row in non_oracle],
        [float(row["mean_mean_scale_exception_gap"]) for row in non_oracle],
        s=80,
        c=["#005f73" if row["method"] == PRIMARY_METHOD else "#9aa6b2" for row in non_oracle],
    )
    for row in non_oracle:
        plt.text(float(row["mean_mean_average_scaling_gain"]) + 0.002, float(row["mean_mean_scale_exception_gap"]) + 0.002, DISPLAY_NAMES.get(row["method"], row["method"]), fontsize=8)
    plt.xlabel("Average scaling gain")
    plt.ylabel("Scale-exception gap")
    plt.title("When average scaling hides boundary risk")
    plt.tight_layout()
    plt.savefig(FIGURES / "scale_exception_gap_v5.png", dpi=180)
    plt.close()


def row_by_method(rows, method):
    return next(row for row in rows if row["method"] == method)


def decide(hard_metrics, pairwise, ablations, stress_summary, fixed_summary, strongest):
    primary = row_by_method(hard_metrics, PRIMARY_METHOD)
    base = row_by_method(hard_metrics, strongest)
    oracle = row_by_method(hard_metrics, ORACLE_METHOD)
    strongest_pair = next(row for row in pairwise if row["baseline"] == strongest)
    full = next(row for row in ablations if row["ablation"] == "full_boundary_aware_scale_exception_audit_v5")
    removed = [row for row in ablations if row["ablation"] != "full_boundary_aware_scale_exception_audit_v5"]
    best_removed_success = max(removed, key=lambda row: float(row["mean_mean_success"]))
    best_removed_utility = max(removed, key=lambda row: float(row["mean_mean_utility"]))
    max_stress = max(float(row["stress_level"]) for row in stress_summary)
    primary_stress = next(row for row in stress_summary if float(row["stress_level"]) == max_stress and row["method"] == PRIMARY_METHOD)
    strongest_stress = next(row for row in stress_summary if float(row["stress_level"]) == max_stress and row["method"] == strongest)
    strict_budget = min(float(row["risk_budget"]) for row in fixed_summary)
    primary_fixed = next(row for row in fixed_summary if float(row["risk_budget"]) == strict_budget and row["method"] == PRIMARY_METHOD)
    strongest_fixed = next(row for row in fixed_summary if float(row["risk_budget"]) == strict_budget and row["method"] == strongest)

    success_margin = float(primary["mean_mean_success"]) - float(base["mean_mean_success"])
    utility_margin = float(primary["mean_mean_utility"]) - float(base["mean_mean_utility"])
    recall_delta = float(primary["mean_mean_rare_failure_recall"]) - float(base["mean_mean_rare_failure_recall"])
    contact_delta = float(primary["mean_mean_contact_boundary_error"]) - float(base["mean_mean_contact_boundary_error"])
    unsafe_delta = float(primary["mean_mean_unsafe_commitment"]) - float(base["mean_mean_unsafe_commitment"])
    overtrust_delta = float(primary["mean_mean_overtrust_rate"]) - float(base["mean_mean_overtrust_rate"])
    cost_delta = float(primary["mean_mean_intervention_cost"]) - float(base["mean_mean_intervention_cost"])
    tail_delta = float(primary["mean_mean_tail_risk_rate"]) - float(base["mean_mean_tail_risk_rate"])
    ablation_success_margin = float(full["mean_mean_success"]) - float(best_removed_success["mean_mean_success"])
    ablation_utility_margin = float(full["mean_mean_utility"]) - float(best_removed_utility["mean_mean_utility"])
    stress_utility_margin = float(primary_stress["mean_mean_utility"]) - float(strongest_stress["mean_mean_utility"])
    fixed_utility_margin = float(primary_fixed["mean_mean_utility"]) - float(strongest_fixed["mean_mean_utility"])

    gates = {
        "success_gate": success_margin >= 0.030 or utility_margin >= 0.050,
        "diagnostic_gate": recall_delta >= 0.050 or contact_delta <= -0.040,
        "safety_gate": unsafe_delta <= 0.020 and overtrust_delta <= 0.020 and cost_delta <= 0.055 and tail_delta <= 0.020,
        "pairwise_gate": (float(strongest_pair["mean_success_diff"]) > 0 or float(strongest_pair["mean_utility_diff"]) > 0) and int(strongest_pair["wins_utility_over_seeds"]) >= 8,
        "ablation_gate": ablation_success_margin >= 0.015 or ablation_utility_margin >= 0.025,
        "stress_gate": stress_utility_margin >= 0.020,
        "fixed_risk_gate": float(primary_fixed["mean_mean_coverage"]) >= 0.300 and fixed_utility_margin >= 0.020,
        "scope_gate": False,
        "success_margin_vs_strongest": success_margin,
        "utility_margin_vs_strongest": utility_margin,
        "rare_failure_recall_delta_vs_strongest": recall_delta,
        "contact_boundary_error_delta_vs_strongest": contact_delta,
        "unsafe_commitment_delta_vs_strongest": unsafe_delta,
        "overtrust_delta_vs_strongest": overtrust_delta,
        "intervention_cost_delta_vs_strongest": cost_delta,
        "tail_risk_delta_vs_strongest": tail_delta,
        "ablation_success_margin_vs_best_removed_component": ablation_success_margin,
        "ablation_utility_margin_vs_best_removed_component": ablation_utility_margin,
        "stress_utility_margin_at_max_stress": stress_utility_margin,
        "strict_fixed_risk_coverage": float(primary_fixed["mean_mean_coverage"]),
        "strict_fixed_risk_utility_margin": fixed_utility_margin,
        "strongest_non_oracle_baseline": strongest,
        "best_removed_component_success": best_removed_success["ablation"],
        "best_removed_component_utility": best_removed_utility["ablation"],
    }
    local_gates = [
        gates["success_gate"],
        gates["diagnostic_gate"],
        gates["safety_gate"],
        gates["pairwise_gate"],
        gates["ablation_gate"],
        gates["stress_gate"],
        gates["fixed_risk_gate"],
    ]
    if all(local_gates):
        decision = "STRONG_REVISE"
        rationale = "expanded local scale-exception evidence supports the mechanism, but the external robotics scope gate fails"
    else:
        decision = "KILL_ARCHIVE"
        rationale = "the expanded local evidence fails at least one frozen empirical gate"
    return decision, rationale, gates, primary, base, oracle


def write_summary_txt(summary):
    payload, hard_metrics, pairwise, ablations = summary
    combined = sorted(hard_metrics, key=lambda row: float(row["mean_mean_utility"]), reverse=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 107 scale_law_exceptions_robotics v5 expanded evidence rebuild\n")
        handle.write(
            f"Design: {len(TASKS)} tasks x {len(REGIMES)} regimes x {len(SPLITS)} splits x {len(METHODS)} methods, "
            f"{len(SEEDS)} seeds, {EPISODES_PER_CELL} episodes/cell.\n"
        )
        handle.write(f"Terminal decision: {payload['terminal_decision']}\n")
        handle.write(f"ICLR main ready: {payload['iclr_main_ready']}\n")
        handle.write(f"Rationale: {payload['rationale']}\n\n")
        handle.write("Hard-aggregate ranking:\n")
        for row in combined:
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.4f} +/- {float(row['ci95_mean_success']):.4f}, "
                f"utility={float(row['mean_mean_utility']):.4f}, rare_recall={float(row['mean_mean_rare_failure_recall']):.4f}, "
                f"contact_error={float(row['mean_mean_contact_boundary_error']):.4f}, unsafe={float(row['mean_mean_unsafe_commitment']):.4f}, "
                f"overtrust={float(row['mean_mean_overtrust_rate']):.4f}, scale_gap={float(row['mean_mean_scale_exception_gap']):.4f}, "
                f"coverage={float(row['mean_mean_boundary_coverage']):.4f}, regret={float(row['mean_mean_regret_to_oracle']):.4f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in payload["gates"].items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: success_diff={float(row['mean_success_diff']):.4f} +/- {float(row['ci95_success_diff']):.4f}, "
                f"utility_diff={float(row['mean_utility_diff']):.4f} +/- {float(row['ci95_utility_diff']):.4f}, "
                f"utility_wins={row['wins_utility_over_seeds']}/{row['seeds']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda row: float(row["mean_mean_utility"]), reverse=True):
            handle.write(
                f"{row['ablation']}: success={float(row['mean_mean_success']):.4f}, utility={float(row['mean_mean_utility']):.4f}, "
                f"scale_gap={float(row['mean_mean_scale_exception_gap']):.4f}, note={row['interpretation']}\n"
            )


def write_tables(hard_metrics, pairwise, ablations, stress_summary, fixed_summary):
    hard_sorted = sorted(hard_metrics, key=lambda row: float(row["mean_mean_utility"]), reverse=True)
    latex_table(
        RESULTS / "hard_aggregate_table.tex",
        hard_sorted,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_utility", "Util."),
            ("mean_mean_rare_failure_recall", "RareRec."),
            ("mean_mean_contact_boundary_error", "ContactErr."),
            ("mean_mean_unsafe_commitment", "Unsafe"),
            ("mean_mean_scale_exception_gap", "Gap"),
        ],
        "Hard-aggregate scale-exception benchmark.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "SuccDiff"),
            ("mean_utility_diff", "UtilDiff"),
            ("wins_utility_over_seeds", "UtilWins"),
        ],
        "Paired hard-aggregate differences against the v5 audit.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablations, key=lambda row: float(row["mean_mean_utility"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_utility", "Util."),
            ("mean_mean_scale_exception_gap", "Gap"),
            ("mean_mean_boundary_coverage", "Coverage"),
        ],
        "Ablations under combined exception stress.",
    )
    max_stress = max(float(row["stress_level"]) for row in stress_summary)
    stress_rows = sorted([row for row in stress_summary if float(row["stress_level"]) == max_stress], key=lambda row: float(row["mean_mean_utility"]), reverse=True)
    latex_table(
        RESULTS / "max_stress_table.tex",
        stress_rows,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_utility", "Util."),
            ("mean_mean_scale_exception_gap", "Gap"),
            ("mean_mean_unsafe_commitment", "Unsafe"),
        ],
        "Maximum-stress sweep endpoint.",
    )
    strict = min(float(row["risk_budget"]) for row in fixed_summary)
    fixed_rows = sorted([row for row in fixed_summary if float(row["risk_budget"]) == strict], key=lambda row: float(row["mean_mean_utility"]), reverse=True)
    latex_table(
        RESULTS / "fixed_risk_table.tex",
        fixed_rows,
        [
            ("method", "Method"),
            ("mean_mean_coverage", "Coverage"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_utility", "Util."),
            ("mean_mean_risk_score", "Risk"),
        ],
        "Strict fixed-risk budget endpoint.",
    )


def main():
    clean_outputs()
    dataset = build_dataset_summary()
    main_rows, main_group, seed_metrics, summary, hard_seed, hard_metrics = build_main()
    strongest = strongest_non_oracle(hard_metrics)
    pairwise = build_pairwise(hard_seed, hard_metrics, strongest)
    ablation_rows, ablation_seed, ablations = build_ablations()
    stress_rows, stress_seed, stress_summary = build_stress_sweep()
    fixed_rows, fixed_seed, fixed_summary = build_fixed_risk()
    fixed_pairwise = fixed_risk_pairwise(fixed_seed, strongest)
    failure_cases = build_failure_cases(main_group, strongest)
    decision, rationale, gates, primary, base, oracle = decide(hard_metrics, pairwise, ablations, stress_summary, fixed_summary, strongest)

    write_csv(RESULTS / "dataset_summary.csv", rounded(dataset))
    write_csv(RESULTS / "cell_metrics.csv", rounded(main_rows))
    write_csv(RESULTS / "main_group_metrics.csv", rounded(main_group))
    write_csv(RESULTS / "seed_metrics.csv", rounded(seed_metrics))
    write_csv(RESULTS / "metrics.csv", rounded(summary))
    write_csv(RESULTS / "hard_seed_metrics.csv", rounded(hard_seed))
    write_csv(RESULTS / "hard_aggregate_metrics.csv", rounded(hard_metrics))
    write_csv(RESULTS / "hard_pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_cell_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablations))
    write_csv(RESULTS / "stress_sweep_cell_metrics.csv", rounded(stress_rows))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_summary))
    write_csv(RESULTS / "fixed_risk_cell_metrics.csv", rounded(fixed_rows))
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", rounded(fixed_seed))
    write_csv(RESULTS / "fixed_risk_metrics.csv", rounded(fixed_summary))
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", rounded(fixed_pairwise))
    write_csv(RESULTS / "failure_cases.csv", rounded(failure_cases))

    make_figures(hard_metrics, ablations, stress_summary, fixed_summary)
    write_tables(hard_metrics, pairwise, ablations, stress_summary, fixed_summary)

    row_counts = {
        "dataset_summary_rows": len(dataset),
        "main_cell_rows": len(main_rows),
        "main_group_rows": len(main_group),
        "seed_metric_rows": len(seed_metrics),
        "metric_rows": len(summary),
        "hard_seed_rows": len(hard_seed),
        "hard_metric_rows": len(hard_metrics),
        "hard_pairwise_rows": len(pairwise),
        "ablation_cell_rows": len(ablation_rows),
        "ablation_seed_rows": len(ablation_seed),
        "ablation_metric_rows": len(ablations),
        "stress_cell_rows": len(stress_rows),
        "stress_seed_rows": len(stress_seed),
        "stress_metric_rows": len(stress_summary),
        "fixed_risk_cell_rows": len(fixed_rows),
        "fixed_risk_seed_rows": len(fixed_seed),
        "fixed_risk_metric_rows": len(fixed_summary),
        "fixed_risk_pairwise_rows": len(fixed_pairwise),
        "failure_case_rows": len(failure_cases),
    }
    payload = {
        "paper": 107,
        "slug": "scale_law_exceptions_robotics",
        "terminal_decision": decision,
        "iclr_main_ready": False,
        "rationale": rationale,
        "design": {
            "tasks": len(TASKS),
            "regimes": len(REGIMES),
            "splits": len(SPLITS),
            "methods": len(METHODS),
            "seeds": len(SEEDS),
            "episodes_per_cell": EPISODES_PER_CELL,
            "stress_levels": 10,
            "fixed_risk_budgets": 4,
            "ablations": len(ABLATIONS),
        },
        "row_counts": row_counts,
        "strongest_non_oracle_baseline": strongest,
        "primary_method": PRIMARY_METHOD,
        "v4_method": V4_METHOD,
        "oracle_method": ORACLE_METHOD,
        "primary_metrics": {metric.replace("mean_mean_", "", 1): float(primary[metric]) for metric in primary if metric.startswith("mean_mean_")},
        "strongest_non_oracle_metrics": {metric.replace("mean_mean_", "", 1): float(base[metric]) for metric in base if metric.startswith("mean_mean_")},
        "oracle_metrics": {metric.replace("mean_mean_", "", 1): float(oracle[metric]) for metric in oracle if metric.startswith("mean_mean_")},
        "gates": gates,
    }
    (RESULTS / "summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    write_summary_txt((payload, hard_metrics, pairwise, ablations))
    print(f"terminal_decision={decision}")
    print(f"iclr_main_ready={payload['iclr_main_ready']}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"main_cell_rows={len(main_rows)}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
