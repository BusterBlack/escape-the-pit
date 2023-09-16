package team3

import (
	"infra/config"
	"infra/game/agent"
	"infra/game/commons"
	"math"
	"math/rand"

	// "os"
	"strconv"
)

type averageStats struct {
	Health  float64
	Stamina float64
	Attack  float64
	Defence float64
}

type thresholdVals struct {
	Health  float64
	Stamina float64
	Attack  float64
	Defence float64
}

func GetHealthAllAgents(baseAgent agent.BaseAgent) []float64 {
	view := baseAgent.View()
	agentState := view.AgentState()
	var agentHealthMap []float64

	itr := agentState.Iterator()
	for !itr.Done() {
		_, state, _ := itr.Next()

		agentHealthMap = append(agentHealthMap, float64(state.Hp))
	}
	return agentHealthMap
}

func GetStaminaAllAgents(baseAgent agent.BaseAgent) []float64 {
	view := baseAgent.View()
	agentState := view.AgentState()
	var agentStaminaMap []float64

	itr := agentState.Iterator()
	for !itr.Done() {
		_, state, _ := itr.Next()

		agentStaminaMap = append(agentStaminaMap, float64(state.Stamina))
	}
	return agentStaminaMap
}
func GetAttackAllAgents(baseAgent agent.BaseAgent) []float64 {
	view := baseAgent.View()
	agentState := view.AgentState()
	var agentStaminaMap []float64

	itr := agentState.Iterator()
	for !itr.Done() {
		_, state, _ := itr.Next()

		agentStaminaMap = append(agentStaminaMap, float64(state.Attack))
	}
	return agentStaminaMap
}

func GetDefenceAllAgents(baseAgent agent.BaseAgent) []float64 {
	view := baseAgent.View()
	agentState := view.AgentState()
	var agentStaminaMap []float64

	itr := agentState.Iterator()
	for !itr.Done() {
		_, state, _ := itr.Next()

		agentStaminaMap = append(agentStaminaMap, float64(state.Defense))
	}
	return agentStaminaMap
}

func GetHealthTSN(baseAgent agent.BaseAgent, TSN []commons.ID) []float64 {
	view := baseAgent.View()
	agentState := view.AgentState()
	var TSNhealthMap []float64
	// loop through TSN and extract HP
	for _, id := range TSN {
		hiddenState, _ := agentState.Get(id)
		TSNhealthMap = append(TSNhealthMap, float64(hiddenState.Hp))
	}
	return TSNhealthMap
}

func GetStaminaTSN(baseAgent agent.BaseAgent, TSN []commons.ID) []float64 {
	view := baseAgent.View()
	agentState := view.AgentState()
	var TSNstaminaMap []float64
	// loop through TSN and extract Stamina
	for _, id := range TSN {
		hiddenState, _ := agentState.Get(id)
		TSNstaminaMap = append(TSNstaminaMap, float64(hiddenState.Stamina))
	}
	return TSNstaminaMap
}

func GetAttackTSN(baseAgent agent.BaseAgent, TSN []commons.ID) []float64 {
	view := baseAgent.View()
	agentState := view.AgentState()
	var TSNattackMap []float64
	// loop through TSN and extract Attack
	for _, id := range TSN {
		hiddenState, _ := agentState.Get(id)
		TSNattackMap = append(TSNattackMap, float64(hiddenState.Attack))
	}
	return TSNattackMap
}

func GetDefenceTSN(baseAgent agent.BaseAgent, TSN []commons.ID) []float64 {
	view := baseAgent.View()
	agentState := view.AgentState()
	var TSNdefenceMap []float64
	// loop through TSN and extract Defense
	for _, id := range TSN {
		hiddenState, _ := agentState.Get(id)
		TSNdefenceMap = append(TSNdefenceMap, float64(hiddenState.Defense))
	}
	return TSNdefenceMap
}

// func (a *AgentThree) FightTSN(agentMap *immutable.Map[commons.ID, state.HiddenAgentState]) {

// 	// for i, id := range a.TSN {

// 	// 	agentMap.Get

// 	// }

// }

func BordaPercentage(baseAgent agent.BaseAgent, borda [][]int) int {
	for i, v := range borda {
		if strconv.FormatInt(int64(v[0]), 10) == baseAgent.ID() {
			return (i / len(borda)) * 100
		}
	}
	return 100
}

func BoolToInt(b bool) int {
	if b {
		return 1
	} else {
		return 0
	}
}
func AverageArray(in []float64) float64 {
	var total float64 = 0
	for _, value := range in {
		total += value
	}
	return total / float64(len(in))
}

func GetStartingHP() int {
	// n, _ := strconv.ParseUint(os.Getenv("STARTING_HP"), 10, 0)
	n := config.EnvToUint("STARTING_HP", 1000)
	return int(n)
}
func GetStartingStamina() int {
	// n, _ := strconv.ParseUint(os.Getenv("BASE_STAMINA"), 10, 0)
	n := config.EnvToUint("BASE_STAMINA", 2000)
	return int(n)
}

func CreateUtility() map[commons.ID]int {
	u := make(map[commons.ID]int, 7)
	return u
}

func (a *AgentThree) InitUtility(baseAgent agent.BaseAgent) map[commons.ID]int {
	view := baseAgent.View()
	agentState := view.AgentState()
	itr := agentState.Iterator()

	u := make(map[commons.ID]int, 7)

	for !itr.Done() {
		id, _, _ := itr.Next()

		u[id] = rand.Intn(10)
	}
	return u
}

func (a *AgentThree) ResetContacts() {
	for i := range a.contactsLastRound {
		a.contactsLastRound[i] = false
	}
}

// normalize function for agent stats
func normalize4El(x, y, z, w float64) (float64, float64, float64, float64) {
	maxVal := minMax4(true, [...]float64{x, y, z, w})
	minVal := minMax4(false, [...]float64{x, y, z, w})
	return (x - minVal) / (maxVal - minVal), (y - minVal) / (maxVal - minVal), (z - minVal) / (maxVal - minVal), (w - minVal) / (maxVal - minVal)
}

// minimum and maximum finder function
func minMax4(isMax bool, nums [4]float64) float64 {
	ans := nums[0]
	for _, num := range nums[1:] {
		if isMax {
			ans = math.Max(num, ans)
		} else {
			ans = math.Min(num, ans)
		}
	}
	return ans
}

func (a *AgentThree) getGroupAvStats(baseAgent agent.BaseAgent) averageStats {
	var avStats averageStats

	avStats.Health = AverageArray(GetHealthAllAgents(baseAgent))
	avStats.Stamina = AverageArray(GetStaminaAllAgents(baseAgent))
	avStats.Attack = AverageArray(GetAttackAllAgents(baseAgent))
	avStats.Defence = AverageArray(GetDefenceAllAgents(baseAgent))

	return avStats
}

func (a *AgentThree) getMyStats(baseAgent agent.BaseAgent) averageStats {
	agentState := baseAgent.AgentState()
	var avStats averageStats

	avStats.Health = float64(agentState.Hp)
	avStats.Stamina = float64(agentState.Stamina)
	avStats.Attack = float64(agentState.Attack)
	avStats.Defence = float64(agentState.Defense)

	return avStats
}

func (a *AgentThree) getTSNAvStats(baseAgent agent.BaseAgent) averageStats {
	var avStats averageStats

	avStats.Health = AverageArray(GetHealthTSN(baseAgent, a.TSN))
	avStats.Stamina = AverageArray(GetStaminaTSN(baseAgent, a.TSN))
	avStats.Attack = AverageArray(GetAttackTSN(baseAgent, a.TSN))
	avStats.Defence = AverageArray(GetDefenceTSN(baseAgent, a.TSN))

	return avStats
}
