import json
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from . import db
from .models import Trade, Backtest

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.get("/health")
def health():
    return jsonify(status="ok")

@bp.get("/market/<symbol>")
@login_required
def market(symbol):
    # Safe demo feed. Replace this adapter with your licensed live-data provider.
    base = {"XAUUSD": 4380.0, "BTCUSD": 110000.0, "EURUSD": 1.17, "GBPUSD": 1.35}.get(symbol.upper(), 100.0)
    candles = []
    for i in range(100):
        p = base + ((i % 11) - 5) * base * 0.0007
        candles.append({"time": int(datetime.utcnow().timestamp()) - (99-i)*3600,
                        "open": p, "high": p*1.0015, "low": p*0.9985, "close": p*1.0004})
    return jsonify(symbol=symbol.upper(), price=candles[-1]["close"], candles=candles)

@bp.post("/trades")
@login_required
def create_trade():
    d = request.get_json(force=True)
    t = Trade(user_id=current_user.id, symbol=d["symbol"].upper(), side=d["side"].upper(),
              entry=float(d["entry"]), quantity=float(d.get("quantity",1)),
              stop_loss=float(d["stop_loss"]) if d.get("stop_loss") else None,
              take_profit=float(d["take_profit"]) if d.get("take_profit") else None,
              notes=d.get("notes",""))
    db.session.add(t); db.session.commit()
    return jsonify(id=t.id), 201

@bp.delete("/trades/<int:trade_id>")
@login_required
def delete_trade(trade_id):
    t = Trade.query.filter_by(id=trade_id, user_id=current_user.id).first_or_404()
    db.session.delete(t); db.session.commit()
    return jsonify(ok=True)

@bp.post("/backtest")
@login_required
def backtest():
    d = request.get_json(force=True)
    # Deterministic demo backtest engine. Replace data source/strategy adapter for production.
    trades = 20
    wins = 11
    losses = trades - wins
    result = {"trades": trades, "wins": wins, "losses": losses,
              "win_rate": round(wins/trades*100,2), "net_r": 7.4, "max_drawdown_r": -2.1}
    b = Backtest(user_id=current_user.id, name=d.get("name","Test"), symbol=d.get("symbol","XAUUSD"),
                 strategy=d.get("strategy","EMA crossover"), result_json=json.dumps(result))
    db.session.add(b); db.session.commit()
    return jsonify(result=result, id=b.id)


@bp.get("/subscription/status")
@login_required
def subscription_status():
    from .models import Subscription
    sub = Subscription.query.filter_by(user_id=current_user.id).order_by(Subscription.created_at.desc()).first()
    if not sub:
        return jsonify(plan="none", status="inactive")
    return jsonify(plan=sub.plan, status=sub.status, current_period_end=sub.current_period_end.isoformat() if sub.current_period_end else None)

@bp.post("/subscription/request")
@login_required
def subscription_request():
    # Provider checkout should be created server-side using provider SDK/webhook.
    # No bank details are accepted or stored here.
    from .models import Subscription
    d = request.get_json(force=True)
    plan = d.get("plan", "").lower()
    if plan not in {"basic", "pro", "prime"}:
        return jsonify(error="Invalid plan"), 400
    sub = Subscription(user_id=current_user.id, plan=plan, status="pending")
    db.session.add(sub); db.session.commit()
    return jsonify(ok=True, plan=plan, status="pending",
                   message="Connect the payment-provider checkout to activate this subscription.")
