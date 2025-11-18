"""
Base Agent class that all specialized agents inherit from.

Provides common functionality for API calls, error handling, and logging.
"""

import json
import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import google.generativeai as genai

from ..utils.config import get_model_config, API_KEY


class BaseAgent(ABC):
    """
    Base class for all extraction and processing agents.
    
    Provides common functionality:
    - Model initialization and configuration
    - Prompt management
    - API call handling with retries
    - Error handling and logging
    - Response parsing
    """
    
    def __init__(
        self,
        agent_name: str,
        model_config: Optional[Dict[str, Any]] = None,
        max_retries: int = 3
    ):
        """
        Initialize the base agent.
        
        Args:
            agent_name: Name of the agent (for logging)
            model_config: Optional custom model configuration
            max_retries: Maximum number of retry attempts
        """
        self.agent_name = agent_name
        self.max_retries = max_retries
        self.logger = self._setup_logger()
        
        # Configure the model
        if model_config is None:
            model_config = get_model_config()
        
        self.model_config = model_config
        self.model_name = model_config["model_name"]
        
        # Initialize Gemini
        if not API_KEY:
            raise ValueError("GOOGLE_API_KEY not set. Please set it in your environment.")
        
        genai.configure(api_key=API_KEY)
        
        # Create model instance
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": model_config.get("temperature", 0.1),
                "top_p": model_config.get("top_p", 0.95),
                "top_k": model_config.get("top_k", 40),
                "max_output_tokens": model_config.get("max_output_tokens", 8192),
            }
        )
        
        self.logger.info(f"Initialized {agent_name} with model {self.model_name}")
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the agent."""
        logger = logging.getLogger(f"Agent.{self.agent_name}")
        logger.setLevel(logging.INFO)
        
        # Console handler
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent.
        
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing method for the agent.
        
        Must be implemented by subclasses.
        
        Args:
            input_data: Input data for processing
            
        Returns:
            Processed output data
        """
        pass
    
    def call_model(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        json_mode: bool = True
    ) -> str:
        """
        Call the model with retry logic.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt (uses default if not provided)
            json_mode: Whether to expect JSON output
            
        Returns:
            Model response text
        """
        if system_prompt is None:
            system_prompt = self.get_system_prompt()
        
        # Combine system and user prompts
        full_prompt = f"{system_prompt}\n\n{prompt}"
        
        for attempt in range(self.max_retries):
            try:
                self.logger.debug(f"Calling model (attempt {attempt + 1}/{self.max_retries})")
                
                response = self.model.generate_content(full_prompt)
                
                if not response or not response.text:
                    raise ValueError("Empty response from model")
                
                response_text = response.text.strip()
                
                # If JSON mode, validate it's valid JSON
                if json_mode:
                    # Try to parse to validate
                    try:
                        json.loads(response_text)
                    except json.JSONDecodeError:
                        # Try to extract JSON from markdown code blocks
                        response_text = self._extract_json_from_markdown(response_text)
                
                self.logger.debug(f"Model call successful")
                return response_text
                
            except Exception as e:
                self.logger.warning(f"Model call attempt {attempt + 1} failed: {str(e)}")
                
                if attempt == self.max_retries - 1:
                    self.logger.error(f"All retry attempts failed")
                    raise
        
        raise RuntimeError(f"Failed to get response after {self.max_retries} attempts")
    
    def _extract_json_from_markdown(self, text: str) -> str:
        """
        Extract JSON from markdown code blocks if present.
        
        Args:
            text: Text that may contain JSON in markdown
            
        Returns:
            Extracted JSON string
        """
        import re
        
        # Look for ```json ... ``` or ``` ... ```
        patterns = [
            r'```json\s*(.*?)\s*```',
            r'```\s*(.*?)\s*```',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                potential_json = match.group(1).strip()
                try:
                    json.loads(potential_json)
                    return potential_json
                except json.JSONDecodeError:
                    continue
        
        # If no markdown blocks, return original
        return text
    
    def parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON response from model.
        
        Args:
            response_text: Text response from model
            
        Returns:
            Parsed JSON object
        """
        try:
            # First try direct parsing
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try extracting from markdown
            cleaned_text = self._extract_json_from_markdown(response_text)
            return json.loads(cleaned_text)
    
    def validate_output(self, output: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        Validate that output contains required fields.
        
        Args:
            output: Output dictionary to validate
            required_fields: List of required field names
            
        Returns:
            True if valid, False otherwise
        """
        for field in required_fields:
            if field not in output:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        return True
    
    def log_stats(self, stats: Dict[str, Any]) -> None:
        """
        Log processing statistics.
        
        Args:
            stats: Statistics dictionary
        """
        self.logger.info(f"{self.agent_name} Stats:")
        for key, value in stats.items():
            self.logger.info(f"  {key}: {value}")


class ExtractionAgent(BaseAgent):
    """
    Base class for extraction agents (Gap, Variable, Technique, Finding).
    
    Provides common extraction functionality.
    """
    
    def __init__(self, agent_name: str, extraction_type: str, **kwargs):
        """
        Initialize extraction agent.
        
        Args:
            agent_name: Name of the agent
            extraction_type: Type of extraction (gaps, variables, etc.)
            **kwargs: Additional arguments for BaseAgent
        """
        super().__init__(agent_name, **kwargs)
        self.extraction_type = extraction_type
    
    def extract_items(
        self,
        pdf_text: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract items from PDF text.
        
        Args:
            pdf_text: Preprocessed PDF text
            context: Optional additional context
            
        Returns:
            List of extracted items
        """
        # To be implemented by subclasses
        raise NotImplementedError
    
    def validate_extraction(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate extracted items.
        
        Args:
            items: List of extracted items
            
        Returns:
            Validation result with errors and warnings
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "item_count": len(items)
        }
        
        # Check minimum count
        if len(items) == 0:
            validation_result["warnings"].append(
                f"No {self.extraction_type} extracted"
            )
        
        # Validate each item has required fields
        required_fields = self._get_required_fields()
        for i, item in enumerate(items):
            for field in required_fields:
                if field not in item:
                    validation_result["errors"].append(
                        f"Item {i}: Missing required field '{field}'"
                    )
                    validation_result["valid"] = False
        
        return validation_result
    
    def _get_required_fields(self) -> List[str]:
        """Get required fields for this extraction type."""
        # Override in subclasses
        return ["context", "thoughts", "summary", "thematicCategorization"]


if __name__ == "__main__":
    # Test basic functionality
    print("BaseAgent class loaded successfully")
    print(f"Available methods: {[m for m in dir(BaseAgent) if not m.startswith('_')]}")
