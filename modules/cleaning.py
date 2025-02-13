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
		

	# Function to standardize numbers (dates, percentages, monetary values, etc.)
	def process_numbers(text):
		"""Detects and standardizes dates, money, percentages, and measurements."""
		if not isinstance(text, str):
			return text

		# Detect and standardize dates
		date_patterns = [r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', r'\b\d{4}-\d{2}-\d{2}\b', r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b']
		for pattern in date_patterns:
			matches = re.findall(pattern, text)
			for match in matches:
				try:
					standardized_date = parser.parse(match).strftime("%Y-%m-%d")
					text = text.replace(match, standardized_date)
				except:
					pass 

		# Standardize phone numbers (removing non-numeric characters except + for country codes)
		text = re.sub(r'\b\+?(\d{1,3})?[-.\s]?(\d{2,3})[-.\s]?(\d{3})[-.\s]?(\d{4,6})\b', r'+\1\2\3\4', text)

		# Remove currency symbols but keep the value
		text = re.sub(r'[\$€£¥₹KShKES]', '', text)

		# Standardize percentages (ensure space before %)
		text = re.sub(r'(\d+)%', r'\1 %', text)

		# Standardize measurements (space between number and unit)
		text = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', text)

		return text
