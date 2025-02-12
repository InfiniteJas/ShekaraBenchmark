import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from collections import defaultdict
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer

class KazakhBenchEvaluator:
    """
    Evaluator for testing language models on Kazakh language tasks.
    Supports multiple question types and provides detailed scoring metrics.
    """

    def __init__(
        self, 
        benchmark_path: str = "benchmarks",
        cache_results: bool = True,
        verbose: bool = False
    ):
        """
        Initialize the evaluator with configuration parameters.

        Args:
            benchmark_path (str): Path to benchmark files
            cache_results (bool): Whether to cache evaluation results
            verbose (bool): Whether to print detailed logs
        """
        self.benchmark_path = Path(benchmark_path)
        self.cache_results = cache_results
        self.verbose = verbose
        
        # Initialize scoring weights
        self.weights = {
            "linguistic": 0.3,
            "logical": 0.25,
            "mathematical": 0.25,
            "cultural": 0.1,
            "contextual": 0.1
        }
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO if verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Load tasks and initialize cache
        self.tasks = self._load_tasks()
        self._results_cache = defaultdict(dict)
        
        # Initialize scorers
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])

    def _load_tasks(self) -> Dict[str, List[Dict]]:
        """
        Load all benchmark tasks from JSON files.
        
        Returns:
            Dict[str, List[Dict]]: Dictionary of tasks by category
        """
        tasks = {}
        try:
            for category in self.weights.keys():
                category_path = self.benchmark_path / category
                if category_path.exists():
                    tasks[category] = []
                    for task_file in category_path.glob("*.json"):
                        with open(task_file, "r", encoding="utf-8") as f:
                            task_data = json.load(f)
                            if isinstance(task_data, dict) and "tasks" in task_data:
                                tasks[category].extend(task_data["tasks"])
                            elif isinstance(task_data, list):
                                tasks[category].extend(task_data)
                            else:
                                self.logger.warning(f"Unexpected format in {task_file}")
                    
                    self.logger.info(f"Loaded {len(tasks[category])} tasks for {category}")
                else:
                    self.logger.warning(f"Category directory not found: {category}")
        except Exception as e:
            self.logger.error(f"Error loading tasks: {str(e)}")
            raise
            
        return tasks

    def evaluate_response(self, response: str, task: Dict) -> Tuple[float, Dict]:
        """
        Evaluate a single response based on task type.
        
        Args:
            response (str): Model's response
            task (Dict): Task definition
            
        Returns:
            Tuple[float, Dict]: Score and detailed metrics
        """
        metrics = {}
        
        try:
            if task["type"] == "MCQ":
                score = self._evaluate_mcq(response, task)
                metrics["correct"] = score
            elif task["type"] == "FRQ":
                score, frq_metrics = self._evaluate_frq(response, task)
                metrics.update(frq_metrics)
            elif task["type"] == "RT":
                score, rt_metrics = self._evaluate_reasoning(response, task)
                metrics.update(rt_metrics)
            else:
                self.logger.warning(f"Unknown task type: {task['type']}")
                return 0.0, {}
                
            metrics["final_score"] = score
            return score, metrics
            
        except Exception as e:
            self.logger.error(f"Error evaluating response: {str(e)}")
            return 0.0, {"error": str(e)}

    def _evaluate_mcq(self, response: str, task: Dict) -> float:
        """
        Evaluate multiple choice question response.
        
        Args:
            response (str): Model's response
            task (Dict): Task definition
            
        Returns:
            float: Score (1.0 for correct, 0.0 for incorrect)
        """
        # Clean and normalize response
        cleaned_response = response.strip().upper()
        correct_answer = task["correct"].strip().upper()
        
        # Check if response contains the correct option letter
        is_correct = cleaned_response == correct_answer or \
                    f"({correct_answer})" in cleaned_response or \
                    f"{correct_answer})" in cleaned_response
                    
        return 1.0 if is_correct else 0.0

    def _evaluate_frq(self, response: str, task: Dict) -> Tuple[float, Dict]:
        """
        Evaluate free response question using multiple metrics.
        
        Args:
            response (str): Model's response
            task (Dict): Task definition
            
        Returns:
            Tuple[float, Dict]: Score and detailed metrics
        """
        metrics = {}
        reference = task["reference_answer"]
        
        # Calculate BLEU score
        reference_tokens = reference.split()
        response_tokens = response.split()
        bleu_score = sentence_bleu([reference_tokens], response_tokens)
        metrics["bleu"] = bleu_score
        
        # Calculate ROUGE scores
        rouge_scores = self.rouge_scorer.score(reference, response)
        metrics["rouge1"] = rouge_scores["rouge1"].fmeasure
        metrics["rouge2"] = rouge_scores["rouge2"].fmeasure
        metrics["rougeL"] = rouge_scores["rougeL"].fmeasure
        
        # Calculate final score as weighted average
        final_score = 0.4 * bleu_score + \
                     0.2 * metrics["rouge1"] + \
                     0.2 * metrics["rouge2"] + \
                     0.2 * metrics["rougeL"]
                     
        return final_score, metrics

    def _evaluate_reasoning(self, response: str, task: Dict) -> Tuple[float, Dict]:
        """
        Evaluate reasoning task response.
        
        Args:
            response (str): Model's response
            task (Dict): Task definition
            
        Returns:
            Tuple[float, Dict]: Score and detailed metrics
        """
        metrics = {}
        
        # Check for required reasoning steps
        required_steps = task.get("reasoning_steps", [])
        response_lower = response.lower()
        
        # Calculate step coverage
        steps_found = sum(1 for step in required_steps 
                         if any(sent.strip() for sent in response_lower.split('.')
                               if step.lower() in sent))
        step_coverage = steps_found / len(required_steps) if required_steps else 0
        metrics["step_coverage"] = step_coverage
        
        # Calculate answer correctness using FRQ evaluation
        if "reference_answer" in task:
            correctness, frq_metrics = self._evaluate_frq(response, task)
            metrics["answer_correctness"] = correctness
            metrics.update({f"answer_{k}": v for k, v in frq_metrics.items()})
        else:
            correctness = 0
            metrics["answer_correctness"] = 0
            
        # Final score combines step coverage and correctness
        final_score = 0.6 * step_coverage + 0.4 * correctness
        
        return final_score, metrics

    def evaluate_model(
        self, 
        model: Any, 
        categories: Optional[List[str]] = None,
        batch_size: int = 1
    ) -> Dict:
        """
        Evaluate model on all or selected categories.
        
        Args:
            model: Model to evaluate
            categories: List of categories to evaluate (None for all)
            batch_size: Number of tasks to process at once
            
        Returns:
            Dict: Evaluation results with scores and metrics
        """
        if categories is None:
            categories = list(self.weights.keys())
            
        results = {
            "category_scores": {},
            "detailed_metrics": defaultdict(list),
            "errors": []
        }
        
        for category in categories:
            if category not in self.tasks:
                self.logger.warning(f"Category not found: {category}")
                continue
                
            category_scores = []
            category_metrics = defaultdict(list)
            
            # Process tasks in batches
            tasks = self.tasks[category]
            for i in range(0, len(tasks), batch_size):
                batch = tasks[i:i + batch_size]
                
                try:
                    # Get model responses
                    responses = self._get_model_responses(model, batch)
                    
                    # Evaluate each response
                    for task, response in zip(batch, responses):
                        score, metrics = self.evaluate_response(response, task)
                        category_scores.append(score)
                        
                        for metric, value in metrics.items():
                            category_metrics[metric].append(value)
                            
                except Exception as e:
                    error_msg = f"Error processing batch in {category}: {str(e)}"
                    self.logger.error(error_msg)
                    results["errors"].append(error_msg)
            
            # Calculate category statistics
            if category_scores:
                results["category_scores"][category] = np.mean(category_scores)
                for metric, values in category_metrics.items():
                    results["detailed_metrics"][f"{category}_{metric}"] = {
                        "mean": np.mean(values),
                        "std": np.std(values),
                        "min": np.min(values),
                        "max": np.max(values)
                    }
        
        # Calculate weighted average
        results["weighted_average"] = self._calculate_weighted_score(
            results["category_scores"]
        )
        
        # Calculate confidence intervals
        results["confidence_intervals"] = self._calculate_confidence_intervals(
            results["category_scores"]
        )
        
        # Cache results if enabled
        if self.cache_results:
            model_id = self._get_model_identifier(model)
            self._results_cache[model_id] = results
            
        return results

    def _get_model_responses(self, model: Any, tasks: List[Dict]) -> List[str]:
        """
        Get responses from model for a batch of tasks.
        
        Args:
            model: Model to evaluate
            tasks: List of tasks
            
        Returns:
            List[str]: Model responses
        """
        responses = []
        for task in tasks:
            try:
                # Format prompt based on task type
                prompt = self._format_prompt(task)
                
                # Get model response
                if hasattr(model, "generate_text"):
                    response = model.generate_text(prompt)
                elif callable(model):
                    response = model(prompt)
                else:
                    response = str(model(prompt))
                    
                responses.append(response)
                
            except Exception as e:
                self.logger.error(f"Error getting model response: {str(e)}")
                responses.append("")
                
        return responses

    def _format_prompt(self, task: Dict) -> str:
        """
        Format task into a prompt for the model.
        
        Args:
            task (Dict): Task definition
            
        Returns:
            str: Formatted prompt
        """
        prompt = task["question"]
        
        if task["type"] == "MCQ":
            options = "\n".join(task["options"])
            prompt = f"{prompt}\n\nТаңдаулар:\n{options}"
        
        return prompt

    def _calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        """
        Calculate weighted average of category scores.
        
        Args:
            scores (Dict[str, float]): Category scores
            
        Returns:
            float: Weighted average score
        """
        weighted_sum = 0.0
        weight_sum = 0.0
        
        for category, score in scores.items():
            if category in self.weights:
                weighted_sum += score * self.weights[category]
                weight_sum += self.weights[category]
                
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0

    def _calculate_confidence_intervals(
        self, 
        scores: Dict[str, float], 
        confidence: float = 0.95
    ) -> Dict[str, Dict[str, float]]:
        """
        Calculate confidence intervals for scores.
        
        Args:
            scores (Dict[str, float]): Category scores
            confidence (float): Confidence level
            
        Returns:
            Dict[str, Dict[str, float]]: Confidence intervals
        """
        intervals = {}
        z_score = 1.96  # 95% confidence interval
        
        for category, score in scores.items():
            if category in self.tasks and len(self.tasks[category]) > 0:
                n = len(self.tasks[category])
                margin = z_score * np.sqrt((score * (1 - score)) / n)
                
                intervals[category] = {
                    "lower": max(0.0, score - margin),
                    "upper": min(1.0, score + margin)
                }
                
        return intervals

    def _get_model_identifier(self, model: Any) -> str:
        """Get unique identifier for model."""
        return getattr(model, "name", str(model))

    def get_cached_results(self, model: Any) -> Optional[Dict]:
        """Get cached results for model if available."""
        model_id = self._get_model_identifier(model)
        return self._results_cache.get(model_id)

    def clear_cache(self):
        """Clear results cache."""
        self._results_cache.clear()
