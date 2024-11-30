import json
import os
import sys

def split_json_file(input_file, max_words=30000, output_dir=""):
    """
    Split a JSON file with extremely strict word count limits.

    Args:
        input_file (str): Path to the input JSON file
        max_words (int, optional): Maximum number of words per output file. Defaults to 30000.
        output_dir (str, optional): Directory to save output files. Defaults to same directory as input file.
    
    Returns:
        list: Paths to the generated output files
    """
    # Determine output directory
    if output_dir is None:
        output_dir = os.path.dirname(input_file) or '.'
    os.makedirs(output_dir, exist_ok=True)

    # Read the entire JSON file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

    # Ensure data is a list
    if not isinstance(data, list):
        data = [data]

    def word_count(obj):
        """Calculate word count for any object"""
        if isinstance(obj, str):
            return len(obj.split())
        elif isinstance(obj, dict):
            return sum(word_count(v) for v in obj.values())
        elif isinstance(obj, list):
            return sum(word_count(item) for item in obj)
        return 0

    output_files = []
    current_chunk = []
    current_word_count = 0
    file_counter = 1

    for item in data:
        item_word_count = word_count(item)
        
        # If this single item is larger than max_words, we'll split it
        if item_word_count > max_words:
            # Split the item recursively if it's a complex object
            def split_item(obj):
                if isinstance(obj, str):
                    # Split strings directly
                    words = obj.split()
                    chunks = []
                    for i in range(0, len(words), max_words):
                        chunks.append(' '.join(words[i:i+max_words]))
                    return chunks
                elif isinstance(obj, dict):
                    # For dictionaries, split each value independently
                    split_dict = {}
                    for k, v in obj.items():
                        split_dict[k] = split_item(v)
                    return split_dict
                elif isinstance(obj, list):
                    # For lists, split each item
                    return [split_item(subitem) for subitem in obj]
                return obj

            # Split the oversized item
            split_items = split_item(item)
            
            # If it's a list of chunks, we need to handle it differently
            if isinstance(split_items, list):
                for subitem in split_items:
                    if current_word_count + word_count(subitem) > max_words:
                        # Write current chunk
                        output_path = os.path.join(output_dir, f'split{file_counter}.json')
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(current_chunk, f, indent=2)
                        output_files.append(output_path)
                        
                        # Reset
                        current_chunk = []
                        current_word_count = 0
                        file_counter += 1
                    
                    current_chunk.append(subitem)
                    current_word_count += word_count(subitem)
            else:
                # Rare case of a non-list split result
                current_chunk.append(split_items)
                current_word_count += word_count(split_items)
        else:
            # Normal item processing
            if current_word_count + item_word_count > max_words:
                # Write current chunk
                output_path = os.path.join(output_dir, f'split{file_counter}.json')
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(current_chunk, f, indent=2)
                output_files.append(output_path)
                
                # Reset
                current_chunk = []
                current_word_count = 0
                file_counter += 1
            
            current_chunk.append(item)
            current_word_count += item_word_count

    # Write the last chunk if not empty
    if current_chunk:
        output_path = os.path.join(output_dir, f'split{file_counter}.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(current_chunk, f, indent=2)
        output_files.append(output_path)

    # Print summary
    print(f"Split into {len(output_files)} files:")
    for file in output_files:
        # Check file size of each split
        file_size = os.path.getsize(file)
        print(f"{file}: {file_size} bytes")

    return output_files

# Command-line usage
if __name__ == '__main__':
    # Check if input file is provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file> [max_words]")
        sys.exit(1)

    # Get input file from command line
    input_file = sys.argv[1]

    # Optional: custom word limit
    max_words = 30000
    if len(sys.argv) > 2:
        try:
            max_words = int(sys.argv[2])
        except ValueError:
            print("Invalid word limit. Using default 30,000.")

    # Split the file
    split_files = split_json_file(input_file, max_words)