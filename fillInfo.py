import os
import re

input_folder = "output"
output_folder = "outputs_extracted"

os.makedirs(output_folder, exist_ok=True)

header_pattern = r"Código\s+Referência\s+interna\s+Descrição\s+Qt\s+Unidade\s+Preço\s+Unitário\s+(Valor\s+Total|Valor\s+Total\s*)"

# 
#  Fix down below if missing info/ invalid
# 
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"extracted_{filename}")
        
        with open(input_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        content_normalized = " ".join(line.strip() for line in lines)
        
        matches = list(re.finditer(header_pattern, content_normalized))
        
        extracted_blocks = []
        for match in matches:
            match_start_line = None

            for i, line in enumerate(lines):
                if match.group(0) in " ".join(line.strip() for line in lines[i:i + 10]):
                    match_start_line = i
                    break

            if match_start_line is not None:
                # Change 20 to a bigger number if needed. Then fix with UN (unit+2) to grab lines. This fixes dynamic description fetching
                block = lines[match_start_line+10:match_start_line + 20]
                extracted_blocks.append("".join(block))

        if extracted_blocks:
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write("\n\n".join(extracted_blocks))
            print(f"Extracted content written to {output_path}")
        else:
            print(f"No matches found in {filename}.")