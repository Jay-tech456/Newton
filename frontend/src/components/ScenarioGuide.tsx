import { Car, AlertTriangle, Cloud, Users, Zap, ArrowRight } from 'lucide-react'

interface Scenario {
  id: string
  name: string
  icon: React.ReactNode
  description: string
  dataset: string
  keyEvents: string[]
  howToInteract: string[]
  expectedOutcome: string
  color: string
}

const scenarios: Scenario[] = [
  {
    id: 'highway',
    name: 'Highway Cruise',
    icon: <Car className="w-6 h-6" />,
    description: 'Normal highway driving with lane changes and adaptive cruise control',
    dataset: 'highway_cruise.zip',
    keyEvents: [
      'Lane change maneuvers',
      'Following distance management',
      'Speed adaptation (25 m/s)'
    ],
    howToInteract: [
      'Upload the highway_cruise.zip dataset',
      'Ask the AI: "What events were detected?"',
      'Select a lane change event from the timeline',
      'Ask: "Analyze this event" to compare safety vs performance strategies',
      'Review how SafetyLab prioritizes safe distances vs PerformanceLab optimizes efficiency'
    ],
    expectedOutcome: 'See how the system balances smooth lane changes with maintaining safe following distances',
    color: 'from-blue-500 to-blue-600'
  },
  {
    id: 'urban',
    name: 'Urban Navigation',
    icon: <Users className="w-6 h-6" />,
    description: 'City driving with pedestrians and complex intersections',
    dataset: 'urban_navigation.zip',
    keyEvents: [
      'Pedestrian detection',
      'Emergency braking for pedestrians',
      'Urban speed limits (10 m/s)',
      'Crosswalk navigation'
    ],
    howToInteract: [
      'Upload the urban_navigation.zip dataset',
      'Look for pedestrian events in the timeline',
      'Ask: "Show me the pedestrian events"',
      'Run analysis on a pedestrian crossing event',
      'Compare how each lab handles pedestrian safety vs traffic flow'
    ],
    expectedOutcome: 'Understand how the system prioritizes pedestrian safety while maintaining traffic efficiency',
    color: 'from-purple-500 to-pink-600'
  },
  {
    id: 'emergency',
    name: 'Emergency Braking',
    icon: <AlertTriangle className="w-6 h-6" />,
    description: 'Sudden obstacle detection requiring immediate response',
    dataset: 'emergency_braking.zip',
    keyEvents: [
      'Sudden obstacle appearance',
      'Rapid deceleration',
      'Critical safety event',
      'High-speed approach (25 m/s)'
    ],
    howToInteract: [
      'Upload the emergency_braking.zip dataset',
      'Ask: "What critical events happened?"',
      'Select the sudden brake event',
      'Run analysis to see emergency response strategies',
      'Compare reaction times and braking distances between labs'
    ],
    expectedOutcome: 'See how the system handles life-critical situations with millisecond-level decision making',
    color: 'from-red-500 to-orange-600'
  },
  {
    id: 'weather',
    name: 'Weather Adaptation',
    icon: <Cloud className="w-6 h-6" />,
    description: 'Driving through changing weather conditions',
    dataset: 'weather_adaptation.zip',
    keyEvents: [
      'Clear → Rain → Fog progression',
      'Speed adaptation to conditions',
      'Visibility challenges',
      'Sensor reliability changes'
    ],
    howToInteract: [
      'Upload the weather_adaptation.zip dataset',
      'Ask: "How does weather affect driving?"',
      'Select adverse weather events',
      'Analyze how strategies adapt to reduced visibility',
      'Compare conservative vs aggressive approaches in poor conditions'
    ],
    expectedOutcome: 'Learn how the system dynamically adjusts to environmental conditions',
    color: 'from-cyan-500 to-blue-600'
  },
  {
    id: 'merge',
    name: 'Complex Merge',
    icon: <Zap className="w-6 h-6" />,
    description: 'Highway merge with multiple vehicles and cut-in events',
    dataset: 'complex_merge.zip',
    keyEvents: [
      'Multiple vehicle interactions',
      'Cut-in detection',
      'Merge lane navigation',
      'Dynamic traffic scenarios'
    ],
    howToInteract: [
      'Upload the complex_merge.zip dataset',
      'Ask: "Show me the cut-in events"',
      'Select a vehicle cut-in event',
      'Run analysis on multi-vehicle interactions',
      'See how labs handle aggressive vs defensive merging'
    ],
    expectedOutcome: 'Understand complex multi-agent interactions and strategic decision-making',
    color: 'from-green-500 to-emerald-600'
  }
]

export default function ScenarioGuide() {
  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-900 via-primary-600 to-purple-600 bg-clip-text text-transparent mb-3">
          Autonomous Driving Scenarios
        </h2>
        <p className="text-gray-600 text-lg max-w-3xl mx-auto">
          Explore different driving scenarios and learn how to interact with the multi-agent analysis system
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {scenarios.map((scenario, index) => (
          <div
            key={scenario.id}
            className={`card slide-in stagger-${Math.min(index + 1, 5)}`}
            style={{ animationFillMode: 'both' }}
          >
            {/* Header */}
            <div className="flex items-start space-x-4 mb-4">
              <div className={`w-14 h-14 bg-gradient-to-br ${scenario.color} rounded-xl flex items-center justify-center shadow-lg flex-shrink-0`}>
                <div className="text-white">
                  {scenario.icon}
                </div>
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold text-gray-900 mb-1">
                  {scenario.name}
                </h3>
                <p className="text-sm text-gray-600">
                  {scenario.description}
                </p>
              </div>
            </div>

            {/* Dataset */}
            <div className="bg-gray-50 rounded-lg p-3 mb-4">
              <div className="text-xs font-semibold text-gray-500 mb-1">DATASET FILE</div>
              <div className="font-mono text-sm text-primary-600 font-medium">
                {scenario.dataset}
              </div>
            </div>

            {/* Key Events */}
            <div className="mb-4">
              <div className="text-sm font-bold text-gray-900 mb-2">🎯 Key Events</div>
              <div className="space-y-1">
                {scenario.keyEvents.map((event, i) => (
                  <div key={i} className="flex items-start space-x-2 text-sm text-gray-700">
                    <span className="text-primary-500 mt-0.5">•</span>
                    <span>{event}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* How to Interact */}
            <div className="mb-4">
              <div className="text-sm font-bold text-gray-900 mb-2">💬 How to Interact</div>
              <div className="space-y-2">
                {scenario.howToInteract.map((step, i) => (
                  <div key={i} className="flex items-start space-x-2 text-sm">
                    <span className={`inline-flex items-center justify-center w-5 h-5 rounded-full bg-gradient-to-br ${scenario.color} text-white text-xs font-bold flex-shrink-0 mt-0.5`}>
                      {i + 1}
                    </span>
                    <span className="text-gray-700">{step}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Expected Outcome */}
            <div className="bg-gradient-to-br from-primary-50 to-purple-50 rounded-lg p-3 border border-primary-200">
              <div className="flex items-start space-x-2">
                <ArrowRight className="w-4 h-4 text-primary-600 mt-0.5 flex-shrink-0" />
                <div>
                  <div className="text-xs font-bold text-primary-900 mb-1">EXPECTED OUTCOME</div>
                  <div className="text-sm text-gray-700">{scenario.expectedOutcome}</div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* General Tips */}
      <div className="card bg-gradient-to-br from-yellow-50 to-orange-50 border-2 border-yellow-200">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center space-x-2">
          <span>💡</span>
          <span>General Tips for Interaction</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <div className="font-bold text-gray-900 mb-2">Chat Commands</div>
            <ul className="space-y-1 text-sm text-gray-700">
              <li>• "Show my datasets" - List all uploaded datasets</li>
              <li>• "What events were detected?" - View event summary</li>
              <li>• "Analyze this event" - Start multi-agent analysis</li>
              <li>• "How does this work?" - Get system explanation</li>
              <li>• "Help" - Show all available commands</li>
            </ul>
          </div>
          <div>
            <div className="font-bold text-gray-900 mb-2">Analysis Workflow</div>
            <ul className="space-y-1 text-sm text-gray-700">
              <li>• Upload dataset → Events auto-detected</li>
              <li>• Select event from timeline</li>
              <li>• Run analysis → Watch agents compete</li>
              <li>• Judge evaluates both strategies</li>
              <li>• Review insights and recommendations</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Understanding the Results */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-4">🧠 Understanding the Results</h3>
        <div className="space-y-4">
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-red-500 to-orange-600 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-white font-bold text-sm">SL</span>
            </div>
            <div>
              <div className="font-bold text-gray-900">SafetyLab</div>
              <div className="text-sm text-gray-600">
                Prioritizes collision avoidance, safe distances, and conservative maneuvers. 
                Higher scores indicate safer but potentially slower decisions.
              </div>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-white font-bold text-sm">PL</span>
            </div>
            <div>
              <div className="font-bold text-gray-900">PerformanceLab</div>
              <div className="text-sm text-gray-600">
                Optimizes for efficiency, smooth traffic flow, and minimal delays. 
                Higher scores indicate more efficient but potentially riskier decisions.
              </div>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-600 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-white font-bold text-sm">J</span>
            </div>
            <div>
              <div className="font-bold text-gray-900">Judge</div>
              <div className="text-sm text-gray-600">
                Impartially evaluates both approaches based on context, severity, and outcomes. 
                The winning strategy influences future system evolution.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
