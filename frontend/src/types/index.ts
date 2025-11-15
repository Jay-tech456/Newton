export interface Dataset {
  id: number
  name: string
  description?: string
  upload_path: string
  frames_path: string
  telemetry_path: string
  frame_count: number
  duration_seconds: number
  created_at: string
}

export enum EventType {
  CUT_IN = 'cut_in',
  PEDESTRIAN = 'pedestrian',
  ADVERSE_WEATHER = 'adverse_weather',
  CLOSE_FOLLOWING = 'close_following',
  SUDDEN_BRAKE = 'sudden_brake',
  LANE_CHANGE = 'lane_change',
  OTHER = 'other',
}

export interface Event {
  id: number
  dataset_id: number
  event_type: EventType
  start_frame_id: string
  end_frame_id: string
  start_timestamp: number
  end_timestamp: number
  ego_speed_mps?: number
  road_type?: string
  weather?: string
  lead_distance_m?: number
  cut_in_flag: boolean
  pedestrian_flag: boolean
  description?: string
  severity: string
  created_at: string
}

export interface Analysis {
  id: number
  event_id: number
  safety_lab_output: LabOutput
  performance_lab_output: LabOutput
  judge_decision: JudgeDecision
  safety_genome_version: string
  performance_genome_version: string
  new_safety_genome_version?: string
  new_performance_genome_version?: string
  duration_seconds?: number
  created_at: string
}

export interface LabOutput {
  lab_name: string
  research_plan: ResearchPlan
  papers_analyzed: number
  top_papers: Paper[]
  synthesis: Synthesis
  duration_seconds: number
}

export interface ResearchPlan {
  lab_name: string
  event_type: string
  sub_questions: string[]
  search_strategy: string
  keywords: string[]
  priority_dimensions: string[]
}

export interface Paper {
  title: string
  authors: string[]
  venue: string
  year: number
  method_category: string
  extracted_info: Record<string, any>
  critique: Critique
}

export interface Critique {
  scores: Record<string, number>
  strengths: string[]
  weaknesses: string[]
  overall_score: number
}

export interface Synthesis {
  lab_name: string
  event_type: string
  num_papers_analyzed: number
  top_papers: {
    title: string
    score: number
    method_category: string
  }[]
  summary: string
  key_methods: string[]
  deployment_recommendations: string[]
  trade_offs?: Record<string, string>
  confidence_level: string
}

export interface JudgeDecision {
  winner: 'SafetyLab' | 'PerformanceLab' | 'Tie'
  safety_lab_score: number
  performance_lab_score: number
  reasoning: string
  safety_lab_strengths: string[]
  safety_lab_weaknesses: string[]
  performance_lab_strengths: string[]
  performance_lab_weaknesses: string[]
  recommendations_for_improvement: {
    SafetyLab: string[]
    PerformanceLab: string[]
  }
}

export interface Genome {
  id: number
  lab_name: string
  version: string
  genome_data: GenomeData
  parent_version?: string
  change_description?: string
  is_active: number
  created_at: string
}

export interface GenomeData {
  retrieval_preferences: {
    year_window: [number, number]
    venue_weights: Record<string, number>
    keywords: string[]
    method_categories?: string[]
  }
  reading_template: {
    extract_fields: string[]
  }
  critique_focus: {
    dimensions: string[]
    weights: Record<string, number>
  }
  synthesis_style: {
    audience: string
    max_tokens: number
    format: string
    emphasis: string
  }
}

export interface GenomeEvolution {
  lab_name: string
  versions: Genome[]
}
