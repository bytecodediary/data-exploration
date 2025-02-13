import re

class DataCleaner():
	def is_code(text):
    """Detect if text contains code snippets dynamically based on common programming patterns."""
    
    # Check if there are any symbols that are typical for code snippets
    code_symbols = r"[{}\[\]\(\);,=<>+-*/&|!]"
    keywords_patterns = [
        r"\b(def|function|class|interface|public|private|protected|async|await|try|catch|return|import|from|require|module)\b",  
        r"\b(if|else|for|while|switch|case|break|continue|try|catch|finally)\b",  
        r"\b(let|var|const|new|yield|typeof)\b",  
        r"\b(print|console|log|yield|import|export)\b",
    ]
    
    # Search for language-agnostic symbols and keywords
    if isinstance(text, str):
        # Check for code symbols
        if re.search(code_symbols, text):
            return True
        
        # Check for common language-agnostic patterns (keywords)
        if any(re.search(pattern, text) for pattern in keywords_patterns):
            return True
        
        # Check for function signatures (simple regex for detecting functions)
        if re.search(r"\w+\s?\(.*\)\s?{", text):  # Detecting function signatures like `def foo() {...}`
            return True
        
        # Check for basic assignment statements (e.g., `x = 10`)
        if re.search(r"\w+\s?=\s?.+", text):  # General assignment pattern
            return True
        
        # Check for indentation (common in Python, Go, etc.)
        if text.startswith("    ") or "\n    " in text:  # Indentation check for 4 spaces
            return True

    return False
