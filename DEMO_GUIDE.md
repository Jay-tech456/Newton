# 🚗 AutoLab Drive - Self-Evolving AI Demo Guide

## 🎯 How to See Self-Evolution in Action

### 1. **Generate Realistic Datasets**

```bash
cd scripts
./run_generator.sh
```

This creates 5 realistic driving scenarios:
- 🚶 **Urban Pedestrian Crossing** (High severity)
- 🚗 **Highway Lane Change** (Medium severity)  
- 🌧️ **Rainy Emergency Brake** (High severity)
- 🏘️ **Suburban Slow Traffic** (Low severity)
- 🌙 **Night Urban Navigation** (Medium severity)

### 2. **Upload Datasets**

1. Go to `http://localhost:5173`
2. Click "View All Datasets"
3. Upload the generated datasets from `backend/storage/datasets/`

### 3. **Run Multiple Analyses to See Evolution**

#### **First Analysis (Baseline)**
1. Select a high-severity event (e.g., Pedestrian Crossing)
2. Click "Analyze Event"
3. Note the genome versions: **v0.1** for both labs
4. Check the scores (e.g., SafetyLab: 84%, PerformanceLab: 77%)

#### **Second Analysis (Evolution Begins)**
1. Analyze another event from the same or different dataset
2. Watch for genome evolution: **v0.1 → v0.2** ✨
3. The losing lab adapts its strategy!

#### **Third Analysis (Continued Evolution)**
1. Analyze a different severity event
2. See genomes evolve to **v0.3**, **v0.4**, etc.
3. Notice how scores change as strategies improve

### 4. **What to Look For**

#### **🧬 Genome Evolution Tracker**
After each analysis, you'll see:
```
SafetyLab Genome: v0.1 → v0.2 ✨
PerformanceLab Genome: v0.1 → v0.2 ✨
```

This shows the strategies are **self-evolving**!

#### **📊 Score Changes**
- **High-severity events**: SafetyLab should score higher (84% vs 77%)
- **Low-severity events**: PerformanceLab should score higher (83% vs 78%)
- **Over time**: Losing labs improve their scores

#### **🔄 Strategy Adaptations**
The MetaLearner updates strategies by:
- **Adopting keywords** from the winner
- **Adjusting weights** for critique dimensions
- **Updating research focus** based on recommendations

### 5. **Video Demo Flow**

For a compelling demo video:

1. **Show the problem** (0:00-0:30)
   - "Autonomous driving needs safety AND performance"
   - "Traditional approaches optimize one or the other"

2. **Introduce the solution** (0:30-1:00)
   - "AutoLab Drive: Self-evolving multi-agent research"
   - Show the UI with datasets

3. **First analysis** (1:00-2:00)
   - Upload pedestrian crossing dataset
   - Run analysis
   - Show SafetyLab vs PerformanceLab competition
   - Highlight genome v0.1 for both

4. **Show evolution** (2:00-3:00)
   - Run second analysis
   - **Point to genome evolution**: v0.1 → v0.2 ✨
   - "The losing lab learned from the winner!"
   - Show the evolution message

5. **Demonstrate adaptation** (3:00-4:00)
   - Run analysis on different severity event
   - Show how strategies adapt to different scenarios
   - Genome versions continue evolving (v0.3, v0.4)

6. **Results** (4:00-4:30)
   - Show improved scores over time
   - Highlight the self-evolution capability
   - "The system gets smarter with every analysis"

## 🎬 Recording Tips

### **Camera Angles**
1. **Wide shot**: Full UI showing both labs competing
2. **Close-up**: Genome evolution tracker (v0.1 → v0.2 ✨)
3. **Screen recording**: Entire analysis flow

### **Narration Points**
- "Watch as the genome versions evolve..."
- "SafetyLab learned from PerformanceLab and updated its strategy"
- "The system is self-improving without human intervention"
- "Each analysis makes both labs smarter"

### **Visual Highlights**
- Circle the genome evolution with annotation
- Highlight the ✨ sparkle when evolution happens
- Show the green success message
- Point to changing scores across analyses

## 📈 Expected Evolution Pattern

```
Analysis 1: v0.1 vs v0.1 → SafetyLab wins (84% vs 77%)
            ↓
Analysis 2: v0.1 vs v0.2 → PerformanceLab improved! (82% vs 81%)
            ↓
Analysis 3: v0.2 vs v0.2 → Tie (85% vs 85%)
            ↓
Analysis 4: v0.3 vs v0.3 → Both labs evolved, smarter strategies
```

## 🚀 Quick Start

```bash
# 1. Generate datasets
cd scripts && ./run_generator.sh

# 2. Start the system
cd .. && docker-compose up -d

# 3. Open browser
open http://localhost:5173

# 4. Upload and analyze!
```

## 💡 Pro Tips

- **Use different severity events** to show adaptation
- **Run 3-5 analyses** to show clear evolution
- **Point out the genome version changes** explicitly
- **Explain what changed** (keywords, weights, focus areas)
- **Show the evolution message** when it appears

---

**The key insight**: The system doesn't just analyze - it **learns and evolves** from every competition! 🧬✨
