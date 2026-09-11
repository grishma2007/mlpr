"""
Association Mining REST API Blueprint
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

from flask import Blueprint, request, jsonify
from association.apriori_analysis import run_apriori_analysis
from association.fpgrowth_analysis import run_fpgrowth_analysis, compare_apriori_and_fpgrowth

association_bp = Blueprint("association_bp", __name__)

@association_bp.route("/association/apriori", methods=["GET"])
def get_apriori():
    """GET /api/association/apriori - Run Apriori rule mining."""
    min_support = float(request.args.get("min_support", 0.05))
    min_confidence = float(request.args.get("min_confidence", 0.3))
    try:
        results = run_apriori_analysis(min_support=min_support, min_confidence=min_confidence)
        return jsonify({"success": True, "results": results}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@association_bp.route("/association/fpgrowth", methods=["GET"])
def get_fpgrowth():
    """GET /api/association/fpgrowth - Run FP-Growth rule mining."""
    min_support = float(request.args.get("min_support", 0.05))
    min_confidence = float(request.args.get("min_confidence", 0.3))
    try:
        results = run_fpgrowth_analysis(min_support=min_support, min_confidence=min_confidence)
        return jsonify({"success": True, "results": results}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@association_bp.route("/association/benchmark", methods=["GET"])
def get_benchmark():
    """GET /api/association/benchmark - Benchmark Apriori vs FP-Growth."""
    min_support = float(request.args.get("min_support", 0.05))
    min_confidence = float(request.args.get("min_confidence", 0.3))
    try:
        benchmark = compare_apriori_and_fpgrowth(min_support=min_support, min_confidence=min_confidence)
        return jsonify({"success": True, "benchmark": benchmark}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
