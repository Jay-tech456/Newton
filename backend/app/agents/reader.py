"""
Reader Agent
Extracts structured information from papers based on reading template.
"""
from typing import Dict, Any, List


class ReaderAgent:
    """
    Reads and extracts information from papers according to genome's reading template.
    """
    
    def __init__(self, lab_name: str, genome: Dict[str, Any]):
        self.lab_name = lab_name
        self.genome = genome
    
    def read(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract structured information from papers.
        
        Args:
            papers: List of papers from RetrieverAgent
            
        Returns:
            List of papers with extracted fields
        """
        extract_fields = self.genome.get("reading_template", {}).get("extract_fields", [])
        
        extracted_papers = []
        for paper in papers:
            extracted = self._extract_fields(paper, extract_fields)
            extracted_papers.append(extracted)
        
        return extracted_papers
    
    def _extract_fields(self, paper: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """
        Extract specific fields from paper based on template.
        """
        extracted = {
            "title": paper.get("title", ""),
            "authors": paper.get("authors", []),
            "venue": paper.get("venue", ""),
            "year": paper.get("year", 0),
            "method_category": paper.get("method_category", ""),
            "extracted_info": {}
        }
        
        # Extract fields based on template
        for field in fields:
            if field == "method_name":
                extracted["extracted_info"]["method_name"] = paper.get("title", "").split(":")[0]
            
            elif field == "safety_guarantees":
                # Extract safety-related info
                results = paper.get("key_results", {})
                extracted["extracted_info"]["safety_guarantees"] = {
                    "collision_rate": results.get("collision_rate"),
                    "safety_violations": results.get("safety_violations"),
                    "safety_score": results.get("safety_score")
                }
            
            elif field == "failure_modes":
                # Extract from deployment notes
                notes = paper.get("deployment_notes", "")
                extracted["extracted_info"]["failure_modes"] = self._extract_failure_modes(notes)
            
            elif field == "robustness_metrics":
                results = paper.get("key_results", {})
                extracted["extracted_info"]["robustness_metrics"] = {
                    "detection_accuracy_rain": results.get("detection_accuracy_rain"),
                    "detection_accuracy_fog": results.get("detection_accuracy_fog"),
                    "worst_case_performance": results.get("worst_case_performance")
                }
            
            elif field == "performance_metrics":
                results = paper.get("key_results", {})
                extracted["extracted_info"]["performance_metrics"] = {
                    "accuracy": results.get("nuscenes_score") or results.get("map_score"),
                    "fps": results.get("fps"),
                    "latency_ms": results.get("latency_ms"),
                    "planning_time_ms": results.get("planning_time_ms")
                }
            
            elif field == "computational_cost":
                results = paper.get("key_results", {})
                extracted["extracted_info"]["computational_cost"] = {
                    "fps": results.get("fps"),
                    "latency_ms": results.get("latency_ms")
                }
            
            elif field == "benchmark_results":
                results = paper.get("key_results", {})
                extracted["extracted_info"]["benchmark_results"] = results
            
            elif field == "deployment_notes":
                extracted["extracted_info"]["deployment_notes"] = paper.get("deployment_notes", "")
            
            elif field == "limitations":
                # Extract limitations from deployment notes
                notes = paper.get("deployment_notes", "")
                extracted["extracted_info"]["limitations"] = self._extract_limitations(notes)
            
            elif field == "scalability":
                notes = paper.get("deployment_notes", "")
                extracted["extracted_info"]["scalability"] = "scalable" if "scalable" in notes.lower() else "limited"
        
        return extracted
    
    def _extract_failure_modes(self, text: str) -> List[str]:
        """Extract failure modes from text"""
        failure_keywords = ["requires", "limited", "fails", "degrades"]
        failure_modes = []
        
        sentences = text.split(";")
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in failure_keywords):
                failure_modes.append(sentence.strip())
        
        return failure_modes if failure_modes else ["No specific failure modes documented"]
    
    def _extract_limitations(self, text: str) -> List[str]:
        """Extract limitations from text"""
        limitation_keywords = ["requires", "limited", "only suitable", "not suitable"]
        limitations = []
        
        sentences = text.split(";")
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in limitation_keywords):
                limitations.append(sentence.strip())
        
        return limitations if limitations else ["No specific limitations documented"]
