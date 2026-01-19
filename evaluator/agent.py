from evaluator.environment.loader import load_assets
from evaluator.environment.arbitrage_books import generate_books
from evaluator.a2a_client import A2AClient
from evaluator.tasks import (
    portfolio_task,
    portfolio_score,
    regime_task,
    regime_score,
    arbitrage_task,
    arbitrage_score,
    execution_task,
    execution_score,
)
from evaluator.output import write_results

def main():
    # Connect to purple agent
    client = A2AClient("http://localhost:9009")

    # Load environment
    env = load_assets(regime="flash_crash", seed=42)
    
    # Add arbitrage books to environment
    arb_env = generate_books(seed=42)
    env.update(arb_env)

    results = []

    #Portfolio Task 
    task = portfolio_task(env)
    response = client.execute(task)
    score = portfolio_score(response, env)
    results.append(("portfolio", score))

    # Regime Detection Task 
    task = regime_task(env)
    response = client.execute(task)
    score = regime_score(response.get("regime"), env["true_regime"])
    results.append(("regime_detection", score))
    
    #  Arbitrage Task 
    task = arbitrage_task(env)
    response = client.execute(task)
    score = arbitrage_score(response, env)
    results.append(("arbitrage", score))
    
    #  Execution Task 
    task = execution_task(env)
    response = client.execute(task)
    score = execution_score(response, env)
    results.append(("execution", score))

    # Write final results
    write_results("baseline-agent", results)

if __name__ == "__main__":
    main()

