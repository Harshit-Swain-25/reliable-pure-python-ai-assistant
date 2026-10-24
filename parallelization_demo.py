import time
from concurrent.futures import ThreadPoolExecutor


def complete_task(task_name: str) -> str:
    time.sleep(2)
    return f"{task_name} completed"

def run_in_sequentially() -> None:
    start_time = time.perf_counter()
    results = [
        complete_task("Explanation"),
        complete_task("Summary"),
        complete_task("Questions"),

    ]

    elasped_time = time.perf_counter() - start_time
    print("Sequential Results: ")
    for result in results:
        print(result)

    print(f"Sequential time: {elasped_time:.2f} seconds")

def run_in_parallel() -> None:
    """Run three independent tasks concurrently."""
    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(
            executor.map(
                complete_task,
                ["Explanation", "Summary", "Questions"],
            )
        )

    elapsed_time = time.perf_counter() - start_time

    print("\nParallel results:")
    for result in results:
        print(result)

    print(f"Parallel time: {elapsed_time:.2f} seconds")

def main() -> None:
    run_in_sequentially()
    run_in_parallel()

if __name__ == "__main__":
    main()