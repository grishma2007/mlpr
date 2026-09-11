"""
Reinforcement Learning Q-Learning REST API Blueprint
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

from flask import Blueprint, request, jsonify
from rl_demo.q_learning_optimizer import run_rl_simulation

rl_bp = Blueprint("rl_bp", __name__)

@rl_bp.route("/rl/optimize-path", methods=["POST", "GET"])
def optimize_path():
    """
    POST /api/rl/optimize-path
    Runs educational Q-Learning path optimizer simulation.
    """
    data = request.get_json(silent=True) or {}
    episodes = int(data.get("episodes", 300))
    alpha = float(data.get("learning_rate", 0.1))
    gamma = float(data.get("discount_factor", 0.9))
    
    try:
        sim_results = run_rl_simulation(episodes=episodes, alpha=alpha, gamma=gamma)
        return jsonify({"success": True, "simulation": sim_results}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
