#!/usr/bin/env python3
"""
Extract markdown content from OpenAI deep research JSON response.

OpenAI deep research returns a complex nested JSON structure with multiple
output types (reasoning, web_search_call, message). This script extracts
the actual markdown report from the 'message' type content.

Usage:
    python3 extract_json.py INPUT_JSON OUTPUT_MD

Example:
    python3 extract_json.py 99-TMP/OUTPUT/research-raw.json 99-TMP/OUTPUT/research.md
"""

import json
import sys

def extract_research_content(input_file, output_file):
    """Extract markdown content from OpenAI JSON response."""

    # Read the raw JSON response
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Find the message type in output array
    content = ''
    for item in data.get('output', []):
        if item.get('type') == 'message':
            # Extract text from content array
            for content_item in item.get('content', []):
                if content_item.get('type') == 'output_text':
                    content = content_item.get('text', '')
                    break
            if content:
                break

    if not content:
        print('ERROR: No message content found in JSON response')
        print('Expected structure: output[].type="message".content[].type="output_text".text')
        sys.exit(1)

    # Save the extracted markdown
    with open(output_file, 'w') as out:
        out.write(content)

    print(f'✓ Research content extracted successfully')
    print(f'  Input:  {input_file}')
    print(f'  Output: {output_file}')
    print(f'  Size:   {len(content):,} characters')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 extract_json.py INPUT_JSON OUTPUT_MD')
        print('Example: python3 extract_json.py research-raw.json research.md')
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    extract_research_content(input_file, output_file)
