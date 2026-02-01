from .portfolio import generate_task as portfolio_task, score as portfolio_score
from .regime_detection import (
    generate_task as regime_task,
    score as regime_score,
)
from .arbitrage import generate_task as arbitrage_task, score as arbitrage_score
from .execution import generate_task as execution_task, score as execution_score

__all__ = [
    "portfolio_task",
    "portfolio_score",
    "regime_task",
    "regime_score",
    "arbitrage_task",
    "arbitrage_score",
    "execution_task",
    "execution_score",
]
