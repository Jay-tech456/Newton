# 🤖 How Agents Analyze Datasets - Complete Flow

## 📊 Overview

The system uses **9 specialized agents** working in a **self-evolving pipeline** to analyze driving events and improve over time.

---

## 🔄 Complete Analysis Pipeline

```
Dataset Upload → Event Detection → Multi-Agent Analysis → Judge Decision → Meta-Learning → Evolution
```

---

## 1️⃣ **Dataset Upload & Event Detection**

### What Happens:
```python
# User uploads ZIP file with:
# - frames/ (video frames)
# - telemetry.csv (vehicle data)
# - metadata.json (event info)

# System extracts events from telemetry.csv:
event = {
    "event_type": "pedestrian",        # Type of event
    "severity": "high",                # Risk level
    "ego_speed_mps": 8.3,             # Vehicle speed
    "road_type": "urban",             # Environment
    "weather": "clear",               # Conditions
    "lead_distance_m": 15.0,          # Distance to obstacle
    "pedestrian_flag": 1,             # Event flags
    "cut_in_flag": 0,
    "brake_flag": 0
}
```

### Key Files:
- `/backend/app/api/routes.py` - Upload handler
- `/backend/app/services/dataset_processor.py` - Event extraction

---

## 2️⃣ **Multi-Agent Analysis** (Both Labs Run in Parallel)

When you click "Analyze Event", **TWO labs compete**:

### 🛡️ **SafetyLab** (Genome v0.X)
```
Focus: Safety, robustness, worst-case scenarios
Keywords: ["safety verification", "robust perception", "failure modes"]
Weights: {safety: 0.4, robustness: 0.3, performance: 0.3}
```

### ⚡ **PerformanceLab** (Genome v0.X)
```
Focus: Speed, efficiency, optimization
Keywords: ["real-time", "optimization", "computational efficiency"]
Weights: {performance: 0.4, speed: 0.3, safety: 0.3}
```

---

## 3️⃣ **5-Step Research Workflow** (Each Lab)

### **Step 1: Planning** 📋
```python
# PlannerAgent creates research strategy
planner = PlannerAgent(lab_name, genome)
research_plan = planner.plan(event_data)

# Output:
{
    "sub_questions": [
        "What are SOTA safety methods for pedestrian detection?",
        "How to handle edge cases in urban environments?"
    ],
    "keywords": ["pedestrian detection", "safety verification"],
    "search_strategy": "Focus on high-impact safety papers"
}
```

**File**: `/backend/app/agents/planner.py`

---

### **Step 2: Retrieval** 🔍
```python
# RetrieverAgent searches for relevant papers
retriever = RetrieverAgent(lab_name, genome)
papers = retriever.retrieve(research_plan)

# Output: List of 10-20 relevant papers
[
    {
        "title": "Safe RL for Autonomous Driving",
        "authors": ["Smith, J.", "Doe, A."],
        "venue": "CVPR",
        "year": 2023
    },
    ...
]
```

**File**: `/backend/app/agents/retriever.py`

---

### **Step 3: Reading** 📖
```python
# ReaderAgent extracts key information
reader = ReaderAgent(lab_name, genome)
extracted_papers = reader.read(papers)

# Output: Papers with extracted methods
{
    "method_category": "safety_verification",
    "key_techniques": ["reachability analysis", "formal verification"],
    "applicability": "High for urban scenarios"
}
```

**File**: `/backend/app/agents/reader.py`

---

### **Step 4: Critique** ⭐
```python
# CriticAgent evaluates papers based on genome weights
critic = CriticAgent(lab_name, genome)
critiqued_papers = critic.critique(extracted_papers, event_data)

# Output: Scored papers
{
    "scores": {
        "accuracy": 0.92,
        "safety": 0.95,      # High for SafetyLab
        "speed": 0.75,       # Lower priority
        "overall_score": 0.87
    },
    "strengths": ["Strong safety guarantees", "Proven robustness"],
    "weaknesses": ["Computational overhead"]
}
```

**File**: `/backend/app/agents/critic.py`

**Key**: Uses genome weights to score papers differently!

---

### **Step 5: Synthesis** 🎯
```python
# SynthesizerAgent creates final recommendations
synthesizer = SynthesizerAgent(lab_name, genome)
synthesis = synthesizer.synthesize(research_plan, critiqued_papers, event_data)

# Output: Lab's final answer
{
    "summary": "Recommended approach combines robust perception with verified planning",
    "key_methods": [
        "Multi-modal sensor fusion",
        "Model predictive control with safety constraints"
    ],
    "deployment_recommendations": [
        "Implement gradual rollout",
        "Monitor edge cases"
    ],
    "top_papers": [...]
}
```

**File**: `/backend/app/agents/synthesizer.py`

---

## 4️⃣ **Judge Decision** ⚖️

```python
# JudgeAgent compares both labs
judge = JudgeAgent()
decision = judge.judge(safety_output, performance_output, event_data)

# Scoring Criteria (100 points):
# - Relevance (30%): Match to event type
# - Safety (25%): Risk mitigation quality
# - Performance (20%): Computational efficiency
# - Practicality (15%): Real-world applicability
# - Innovation (10%): Novel approaches

# Output:
{
    "winner": "SafetyLab",              # Who won
    "safety_lab_score": 0.84,           # 84%
    "performance_lab_score": 0.77,      # 77%
    "reasoning": "SafetyLab provided superior safety guarantees...",
    "strengths": ["Strong theoretical foundation", "Proven robustness"],
    "weaknesses": ["Computational overhead in verification"]
}
```

**File**: `/backend/app/agents/judge.py`

**Key Logic**:
- High-severity events → SafetyLab advantage
- Low-severity events → PerformanceLab advantage
- Scores reflect actual analysis quality

---

## 5️⃣ **Meta-Learning & Evolution** 🧬

```python
# MetaLearnerAgent updates the losing lab's genome
meta_learner = MetaLearnerAgent()
(new_safety_genome, new_performance_genome, changes) = meta_learner.learn(
    judge_decision,
    safety_genome,
    performance_genome,
    event_data
)

# Evolution Strategy:
# 1. Identify winner's strengths
# 2. Extract successful keywords
# 3. Adjust loser's weights
# 4. Update research focus
# 5. Create new genome version

# Example Evolution:
{
    "version": "v0.2",  # Incremented from v0.1
    "changes": [
        "Added keywords: 'robust perception', 'uncertainty estimation'",
        "Increased safety weight: 0.3 → 0.35",
        "Adopted winner's research strategy"
    ],
    "genome": {
        "keywords": ["safety", "robust perception", "uncertainty"],  # Updated!
        "weights": {"safety": 0.35, "performance": 0.35, "speed": 0.3},  # Adjusted!
        "focus_areas": ["edge case handling", "robust perception"]  # New!
    }
}
```

**File**: `/backend/app/agents/meta_learner.py`

**Key**: The losing lab learns from the winner!

---

## 6️⃣ **Genome Storage & Versioning** 💾

```python
# New genome saved to database
new_genome = StrategyGenome(
    lab_name="SafetyLab",
    version="v0.2",
    genome_data=new_safety_genome,
    is_active=True,
    parent_version="v0.1",
    changes_description="Learned from PerformanceLab's efficiency focus"
)
db.add(new_genome)
db.commit()
```

**Database**: `/backend/app/models/genome.py`

---

## 🎬 Visual Flow in UI

### **Analysis Progress** (What you see):
```
1. 🔍 Analyzing event...
2. 🛡️  SafetyLab analyzing... (5 steps)
3. ⚡ PerformanceLab analyzing... (5 steps)
4. ⚖️  Judge evaluating...
5. 🧬 Meta-learner updating strategies...
6. ✅ Analysis complete!
```

### **Results Display**:
```
Winner: SafetyLab

SafetyLab Score: 84%
PerformanceLab Score: 77%

🧬 Strategy Evolution:
SafetyLab: v0.1 → v0.2 ✨
PerformanceLab: v0.1 (no change)

🎉 Strategies evolved! The labs learned from this analysis.
```

---

## 📈 Evolution Over Time

### **Analysis 1** (Pedestrian, High Severity):
```
SafetyLab (v0.1): 84% ✅ Winner
PerformanceLab (v0.1): 77%
→ PerformanceLab evolves to v0.2 (learns safety focus)
```

### **Analysis 2** (Highway, Low Severity):
```
SafetyLab (v0.1): 78%
PerformanceLab (v0.2): 83% ✅ Winner (improved!)
→ SafetyLab evolves to v0.2 (learns efficiency)
```

### **Analysis 3** (Mixed Scenario):
```
SafetyLab (v0.2): 85% ✅ Winner (improved!)
PerformanceLab (v0.2): 84% (close!)
→ Both labs getting smarter!
```

---

## 🔑 Key Insights

### **1. Genome = Strategy DNA**
```python
genome = {
    "keywords": [...],      # What to search for
    "weights": {...},       # How to evaluate
    "focus_areas": [...]    # Research priorities
}
```

### **2. Each Lab Has Different DNA**
- **SafetyLab**: Prioritizes safety, robustness, worst-case
- **PerformanceLab**: Prioritizes speed, efficiency, optimization

### **3. Competition Drives Evolution**
- Labs compete on every event
- Loser learns from winner
- Both improve over time

### **4. Self-Improving System**
- No human intervention needed
- Strategies adapt to different scenarios
- Gets smarter with every analysis

---

## 📁 Key Files Reference

| Component | File | Purpose |
|-----------|------|---------|
| **Orchestrator** | `services/research_lab.py` | Coordinates entire flow |
| **Planner** | `agents/planner.py` | Creates research strategy |
| **Retriever** | `agents/retriever.py` | Finds relevant papers |
| **Reader** | `agents/reader.py` | Extracts key information |
| **Critic** | `agents/critic.py` | Evaluates papers |
| **Synthesizer** | `agents/synthesizer.py` | Creates recommendations |
| **Judge** | `agents/judge.py` | Compares labs |
| **Meta-Learner** | `agents/meta_learner.py` | Evolves genomes |
| **API** | `api/routes.py` | Handles requests |

---

## 🚀 Try It Yourself!

1. **Upload a dataset** with different severity events
2. **Analyze multiple events** to see evolution
3. **Watch genome versions** increment (v0.1 → v0.2 → v0.3)
4. **See scores improve** as labs learn
5. **Notice adaptation** to different scenarios

The system truly **learns and evolves** with every analysis! 🧬✨
