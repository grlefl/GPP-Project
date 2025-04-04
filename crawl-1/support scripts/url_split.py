import os

#splits url list to files of 100 urls
def split_file(input_file, output_dir="./url_tranco10k_split", chunk_size=100):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r') as f:
        lines = f.readlines()

    total_chunks = (len(lines) + chunk_size - 1) // chunk_size

    for i in range(total_chunks):
        chunk_lines = lines[i * chunk_size : (i + 1) * chunk_size]
        output_file = os.path.join(output_dir, f"{i + 1}.txt")
        with open(output_file, 'w') as f_out:
            f_out.writelines(chunk_lines)
        print(f"Wrote {len(chunk_lines)} lines to {output_file}")

split_file("url/tranco_10000.txt")