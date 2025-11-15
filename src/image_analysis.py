"""
Image Analysis Module for Autonomous Driving Pipeline
Uses YOLO for object detection and computer vision for scene understanding
"""

import cv2
import numpy as np
import torch
from ultralytics import YOLO
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import base64

logger = logging.getLogger(__name__)

@dataclass
class DetectionResult:
    """Single object detection result"""
    class_name: str
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]
    center: Tuple[float, float]
    area: float

@dataclass
class SceneAnalysis:
    """Comprehensive scene analysis results"""
    detections: List[DetectionResult]
    lane_info: Dict
    weather_assessment: str
    visibility_score: float
    obstacle_count: int
    risk_level: str
    depth_estimates: Dict

class ImageAnalyzer:
    """Analyzes autonomous driving images using YOLO and computer vision"""
    
    def __init__(self, config: dict):
        self.config = config
        self.yolo_config = config['yolo']
        self.image_config = config['image_analysis']
        
        # Initialize YOLO model
        self.model = YOLO(self.yolo_config['model_name'])
        
        # Set device
        device = config['embeddings']['device']
        self.model.to(device)
        
        # Classes of interest for autonomous driving
        self.tracked_classes = set(self.yolo_config['classes_to_track'])
        
        logger.info(f"Initialized YOLO model: {self.yolo_config['model_name']}")
    
    def analyze_image(self, image_path: str, frame_telemetry: Dict = None) -> SceneAnalysis:
        """
        Perform comprehensive image analysis
        
        Args:
            image_path: Path to the image file
            frame_telemetry: Telemetry data for this frame
            
        Returns:
            SceneAnalysis object with comprehensive results
        """
        # Load and preprocess image
        image = self._load_image(image_path)
        if image is None:
            return self._create_empty_analysis()
        
        # Perform YOLO detection
        detections = self._detect_objects(image)
        
        # Analyze scene
        lane_info = self._analyze_lanes(image)
        weather_assessment = self._assess_weather(image, frame_telemetry)
        visibility_score = self._calculate_visibility(image)
        obstacle_count = self._count_obstacles(detections)
        risk_level = self._assess_risk(detections, frame_telemetry)
        depth_estimates = self._estimate_depth(detections, image.shape)
        
        return SceneAnalysis(
            detections=detections,
            lane_info=lane_info,
            weather_assessment=weather_assessment,
            visibility_score=visibility_score,
            obstacle_count=obstacle_count,
            risk_level=risk_level,
            depth_estimates=depth_estimates
        )
    
    def _load_image(self, image_path: str) -> Optional[np.ndarray]:
        """Load and preprocess image"""
        if not Path(image_path).exists():
            logger.warning(f"Image file not found: {image_path}")
            return None
        
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            logger.warning(f"Failed to load image: {image_path}")
            return None
        
        # Resize if needed
        target_size = self.image_config['resize_dimensions']
        if image.shape[:2] != target_size[::-1]:  # OpenCV uses (h,w)
            image = cv2.resize(image, target_size)
        
        return image
    
    def _detect_objects(self, image: np.ndarray) -> List[DetectionResult]:
        """Perform YOLO object detection"""
        results = self.model(
            image,
            conf=self.yolo_config['confidence_threshold'],
            iou=self.yolo_config['iou_threshold'],
            max_det=self.yolo_config['max_detections']
        )
        
        detections = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Get class info
                    class_id = int(box.cls)
                    class_name = self.model.names[class_id]
                    
                    # Only track classes of interest
                    if class_name not in self.tracked_classes:
                        continue
                    
                    # Get bbox coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0].cpu().numpy())
                    
                    # Calculate center and area
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    area = (x2 - x1) * (y2 - y1)
                    
                    detection = DetectionResult(
                        class_name=class_name,
                        confidence=confidence,
                        bbox=[float(x1), float(y1), float(x2), float(y2)],
                        center=(float(center_x), float(center_y)),
                        area=float(area)
                    )
                    detections.append(detection)
        
        return detections
    
    def _analyze_lanes(self, image: np.ndarray) -> Dict:
        """Analyze lane markings and road structure"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Canny edge detection
            edges = cv2.Canny(blurred, 50, 150)
            
            # Region of interest (bottom half of image)
            height, width = edges.shape
            roi_vertices = [
                [(0, height), (width, height), (width, height//2), (0, height//2)]
            ]
            roi_edges = self._apply_roi(edges, roi_vertices)
            
            # Hough line detection
            lines = cv2.HoughLinesP(roi_edges, 1, np.pi/180, 50, 50, 50)
            
            # Analyze lines for lane detection
            lane_info = {
                'lines_detected': lines is not None,
                'line_count': len(lines) if lines is not None else 0,
                'lane_width_estimate': self._estimate_lane_width(lines, width) if lines is not None else 0,
                'lane_confidence': min(len(lines) / 10.0, 1.0) if lines is not None else 0.0
            }
            
            return lane_info
            
        except Exception as e:
            logger.warning(f"Lane analysis failed: {e}")
            return {'lines_detected': False, 'line_count': 0, 'lane_width_estimate': 0, 'lane_confidence': 0.0}
    
    def _apply_roi(self, image: np.ndarray, vertices: List) -> np.ndarray:
        """Apply region of interest mask"""
        mask = np.zeros_like(image)
        cv2.fillPoly(mask, vertices, 255)
        masked_image = cv2.bitwise_and(image, mask)
        return masked_image
    
    def _estimate_lane_width(self, lines: np.ndarray, image_width: int) -> float:
        """Estimate lane width from detected lines"""
        if lines is None or len(lines) < 2:
            return 0.0
        
        # Group lines by angle (left vs right lanes)
        left_lines = []
        right_lines = []
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            
            if angle < 0:  # Left lane (negative slope)
                left_lines.append(line[0])
            else:  # Right lane (positive slope)
                right_lines.append(line[0])
        
        # Calculate average lane width
        if len(left_lines) > 0 and len(right_lines) > 0:
            # Simple estimation based on line positions
            left_x = np.mean([line[0] for line in left_lines] + [line[2] for line in left_lines])
            right_x = np.mean([line[0] for line in right_lines] + [line[2] for line in right_lines])
            lane_width_pixels = right_x - left_x
            return (lane_width_pixels / image_width) * 100  # Normalize to 0-100
        
        return 0.0
    
    def _assess_weather(self, image: np.ndarray, telemetry: Dict = None) -> str:
        """Assess weather conditions from image"""
        # Convert to HSV for better color analysis
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Calculate brightness
        brightness = np.mean(hsv[:, :, 2]) / 255.0
        
        # Check for rain (lower contrast, higher saturation in certain ranges)
        saturation = np.mean(hsv[:, :, 1]) / 255.0
        contrast = np.std(image) / 255.0
        
        # Use telemetry if available
        if telemetry and 'weather' in telemetry:
            telemetry_weather = telemetry['weather'].lower()
            if telemetry_weather in ['clear', 'rainy', 'cloudy', 'foggy']:
                return telemetry_weather
        
        # Assess from image characteristics
        if brightness < 0.3:
            return 'dark'
        elif brightness < 0.6 and contrast < 0.2:
            return 'foggy'
        elif contrast < 0.15 and saturation > 0.4:
            return 'rainy'
        elif brightness > 0.8:
            return 'bright'
        else:
            return 'clear'
    
    def _calculate_visibility(self, image: np.ndarray) -> float:
        """Calculate visibility score (0.0 to 1.0)"""
        # Calculate Laplacian variance (measure of blur)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Calculate contrast
        contrast = np.std(image) / 255.0
        
        # Calculate brightness (should be in good range)
        brightness = np.mean(image) / 255.0
        brightness_score = 1.0 - abs(brightness - 0.5) * 2  # Peak at 0.5
        
        # Combine factors
        blur_score = min(laplacian_var / 500.0, 1.0)  # Normalize
        visibility = (blur_score + contrast + brightness_score) / 3.0
        
        return max(0.0, min(1.0, visibility))
    
    def _count_obstacles(self, detections: List[DetectionResult]) -> int:
        """Count relevant obstacles for autonomous driving"""
        obstacle_classes = {'person', 'car', 'truck', 'bus', 'motorcycle', 'bicycle'}
        return sum(1 for d in detections if d.class_name in obstacle_classes)
    
    def _assess_risk(self, detections: List[DetectionResult], telemetry: Dict = None) -> str:
        """Assess risk level based on detections and telemetry"""
        risk_score = 0
        
        # Check for pedestrians
        pedestrians = [d for d in detections if d.class_name == 'person']
        if pedestrians:
            risk_score += len(pedestrians) * 2
        
        # Check for close vehicles
        vehicles = [d for d in detections if d.class_name in ['car', 'truck', 'bus']]
        for vehicle in vehicles:
            # Estimate distance based on bbox size (larger = closer)
            bbox_area_ratio = vehicle.area / (640 * 640)  # Assuming 640x640 input
            if bbox_area_ratio > 0.1:  # Large bbox = close vehicle
                risk_score += 3
            elif bbox_area_ratio > 0.05:
                risk_score += 2
            else:
                risk_score += 1
        
        # Factor in telemetry
        if telemetry:
            # High speed increases risk
            if 'ego_speed_mps' in telemetry:
                speed = telemetry['ego_speed_mps']
                if speed > 30:  # > 108 km/h
                    risk_score += 2
                elif speed > 20:  # > 72 km/h
                    risk_score += 1
            
            # Flags for dangerous situations
            if 'cut_in_flag' in telemetry and telemetry['cut_in_flag']:
                risk_score += 3
            
            if 'pedestrian_flag' in telemetry and telemetry['pedestrian_flag']:
                risk_score += 2
        
        # Determine risk level
        if risk_score >= 8:
            return 'high'
        elif risk_score >= 4:
            return 'medium'
        elif risk_score >= 1:
            return 'low'
        else:
            return 'minimal'
    
    def _estimate_depth(self, detections: List[DetectionResult], image_shape: Tuple) -> Dict:
        """Estimate depth for detected objects"""
        height, width = image_shape[:2]
        depth_estimates = {}
        
        for detection in detections:
            # Simple depth estimation based on object size in image
            bbox_area_ratio = detection.area / (width * height)
            
            # Estimate distance (inverse relationship with size)
            if bbox_area_ratio > 0.1:
                distance = "< 10m"
            elif bbox_area_ratio > 0.05:
                distance = "10-20m"
            elif bbox_area_ratio > 0.02:
                distance = "20-50m"
            else:
                distance = "> 50m"
            
            depth_estimates[detection.class_name] = {
                'distance_category': distance,
                'bbox_area_ratio': bbox_area_ratio,
                'confidence': detection.confidence
            }
        
        return depth_estimates
    
    def _create_empty_analysis(self) -> SceneAnalysis:
        """Create empty analysis for failed image loads"""
        return SceneAnalysis(
            detections=[],
            lane_info={'lines_detected': False, 'line_count': 0, 'lane_width_estimate': 0, 'lane_confidence': 0.0},
            weather_assessment='unknown',
            visibility_score=0.0,
            obstacle_count=0,
            risk_level='unknown',
            depth_estimates={}
        )
