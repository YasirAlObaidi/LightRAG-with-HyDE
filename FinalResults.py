import json

def analyze_evaluation_results(file_path):
    # Read the JSON file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file at {file_path}")
        return

    # Initialize counters for all criteria
    criteria = ['Overall Winner', 'Diversity', 'Empowerment', 'Comprehensiveness']
    counters = {criterion: {'result1_wins': 0, 'result2_wins': 0, 'total_evaluations': 0} for criterion in criteria}

    # Iterate through the results
    for result in results:
        # Skip entries with errors
        if 'error' in result:
            continue

        # Increment total evaluations and count wins for each criterion
        for criterion in criteria:
            try:
                # Increment total evaluations
                counters[criterion]['total_evaluations'] += 1

                # Check the winner
                winner = result.get(criterion, {}).get('Winner', '')
                
                if winner == 'Answer 1':
                    counters[criterion]['result1_wins'] += 1
                elif winner == 'Answer 2':
                    counters[criterion]['result2_wins'] += 1
                else:
                    print(f"Unexpected winner value for {criterion}: {winner}")
            except Exception as e:
                print(f"Error processing {criterion}: {e}")

    # Print and calculate results for each criterion
    print("Detailed Evaluation Results:")
    print("-" * 50)

    for criterion, data in counters.items():
        total = data['total_evaluations']
        result1_wins = data['result1_wins']
        result2_wins = data['result2_wins']
        
        result1_percentage = (result1_wins / total * 100) if total > 0 else 0
        result2_percentage = (result2_wins / total * 100) if total > 0 else 0

        print(f"\n{criterion}:")
        print(f"Result 1 Wins: {result1_wins}/{total} | {result1_percentage:.1f}%")
        print(f"Result 2 Wins: {result2_wins}/{total} | {result2_percentage:.1f}%")

    return counters

if __name__ == "__main__":
    # Replace with the path to your evaluation results JSON file
    clses=["mix","agriculture","cs","legal"]
    for cls in clses:
        print(cls + "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n")
        file_path = f""
        analyze_evaluation_results(file_path)
        print("\n\n\n")