#!/usr/bin/env python3
"""Convert markdown notebook to Jupyter .ipynb format."""

import json
import re

def markdown_to_notebook(md_file, output_file):
    """Convert markdown file with code blocks to Jupyter notebook."""
    
    with open(md_file, 'r') as f:
        content = f.read()
    
    cells = []
    
    # Split by ## Cell markers
    cell_blocks = re.split(r'## Cell \d+:', content)
    
    # First block is metadata/title
    if cell_blocks[0].strip():
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [cell_blocks[0].strip()]
        })
    
    # Process each cell
    for block in cell_blocks[1:]:
        lines = block.strip().split('\n')
        
        # Extract title (first line)
        title = lines[0].strip() if lines else "Cell"
        
        # Find code block
        code_match = re.search(r'```python\n(.*?)\n```', block, re.DOTALL)
        
        if code_match:
            code = code_match.group(1)
            
            # Add markdown cell with title
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"### {title}"]
            })
            
            # Add code cell
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": code.split('\n')
            })
    
    # Create notebook structure
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            },
            "colab": {
                "name": "AISHA RL Training Notebook",
                "provenance": [],
                "collapsed_sections": []
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Write notebook
    with open(output_file, 'w') as f:
        json.dump(notebook, f, indent=1)
    
    print(f"✓ Created {output_file}")

if __name__ == "__main__":
    markdown_to_notebook('AISHA_TRAINING_NOTEBOOK.md', 'AISHA_RL_Training_Colab.ipynb')
