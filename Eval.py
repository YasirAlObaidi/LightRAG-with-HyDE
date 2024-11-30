import re
import json
import os
import time
from openai import OpenAI
import traceback

def batch_eval(query_file, result1_file, result2_file, output_file_path):
    client = OpenAI(api_key="")

    # Read queries
    with open(query_file, "r") as f:
        data = f.read()
    queries = re.findall(r"- Question \d+: (.+)", data)

    # Read result files
    with open(result1_file, "r", encoding="utf-8") as f:
        answers1 = json.load(f)
    answers1 = [i["result"] for i in answers1]

    with open(result2_file, "r", encoding="utf-8") as f:
        answers2 = json.load(f)
    answers2 = [i["result"] for i in answers2]

    # Prepare results list
    evaluation_results = []

    # Total number of comparisons
    total_comparisons = len(queries)
    
    # Start time tracking
    start_time = time.time()

    # Iterate through queries and answers
    for i, (query, answer1, answer2) in enumerate(zip(queries, answers1, answers2), 1):
        print(f"\n{'='*50}")
        print(f"Processing Comparison {i}/{total_comparisons}")
        print(f"Question: {query[:100]}{'...' if len(query) > 100 else ''}")
        print(f"{'='*50}")

        sys_prompt = """
        ---Role---
        You are an expert tasked with evaluating two answers to the same question based on three criteria: **Comprehensiveness**, **Diversity**, and **Empowerment**.
        """

        prompt = f"""
        You will evaluate two answers to the same question based on three criteria: **Comprehensiveness**, **Diversity**, and **Empowerment**.

        - **Comprehensiveness**: How much detail does the answer provide to cover all aspects and details of the question?
        - **Diversity**: How varied and rich is the answer in providing different perspectives and insights on the question?
        - **Empowerment**: How well does the answer help the reader understand and make informed judgments about the topic?

        For each criterion, choose the better answer (either Answer 1 or Answer 2) and explain why. Then, select an overall winner based on these three categories.

        Here is the question:
        {query}

        Here are the two answers:

        **Answer 1:**
        {answer1}

        **Answer 2:**
        {answer2}

        Evaluate both answers using the three criteria listed above and provide detailed explanations for each criterion.

        Output your evaluation in the following JSON format:

        {{
            "Comprehensiveness": {{
                "Winner": "[Answer 1 or Answer 2]",
                "Explanation": "[Provide explanation here]"
            }},
            "Diversity": {{
                "Winner": "[Answer 1 or Answer 2]",
                "Explanation": "[Provide explanation here]"
            }},
            "Empowerment": {{
                "Winner": "[Answer 1 or Answer 2]",
                "Explanation": "[Provide explanation here]"
            }},
            "Overall Winner": {{
                "Winner": "[Answer 1 or Answer 2]",
                "Explanation": "[Summarize why this answer is the overall winner based on the three criteria]"
            }}
        }}
        """

        try:
            # Implement exponential backoff and retry
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Direct API call to get evaluation
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": sys_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        response_format={"type": "json_object"},
                        timeout=60  # 60-second timeout
                    )

                    # Parse the response
                    try:
                        result = json.loads(response.choices[0].message.content)
                        result['query'] = query  # Add query for reference
                        evaluation_results.append(result)
                        
                        # Print success message
                        print(f"\n✅ Comparison {i} Complete")
                        print(f"Overall Winner: {result['Overall Winner']['Winner']}")
                        
                        # Calculate and print estimated time remaining
                        elapsed_time = time.time() - start_time
                        avg_time_per_comparison = elapsed_time / i
                        remaining_comparisons = total_comparisons - i
                        estimated_remaining_time = avg_time_per_comparison * remaining_comparisons
                        
                        print(f"\nProgress: {i}/{total_comparisons}")
                        print(f"Estimated time remaining: {estimated_remaining_time/60:.1f} minutes")
                        
                        break  # Successful, exit retry loop
                    except json.JSONDecodeError:
                        print(f"JSON decode error for query {i}, attempt {attempt+1}")
                        if attempt == max_retries - 1:
                            raise

                except Exception as retry_exc:
                    print(f"Attempt {attempt+1} failed: {str(retry_exc)}")
                    if attempt < max_retries - 1:
                        # Exponential backoff
                        time.sleep(2 ** attempt)
                    else:
                        raise

        except Exception as e:
            print(f"❌ Error processing comparison {i}: {str(e)}")
            traceback.print_exc()
            evaluation_results.append({
                "error": str(e),
                "query": query
            })

        # Add a small delay between requests to avoid rate limiting
        time.sleep(1)

        # Periodically save results to handle potential interruptions
        if i % 10 == 0:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Saved intermediate results after {i} comparisons")

    # Final write of results
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(evaluation_results, f, indent=2, ensure_ascii=False)

    # Calculate total processing time
    total_time = time.time() - start_time
    print(f"\n🏁 Evaluation Complete")
    print(f"Total Time: {total_time/60:.1f} minutes")
    print(f"Evaluation results written to {output_file_path}")

if __name__ == "__main__":
    # Replace with your actual file paths
    
    batch_eval(
        query_file=f"",
        result1_file=f"",
        result2_file=f"",
        output_file_path=f""
    )