package team3

import (
	"infra/game/agent"
	"time"

	"infra/game/commons"
	"math"
	"sort"

	"infra/game/decision"
	"infra/game/state"

	// "infra/logging"
	"math/rand"

	"github.com/benbjohnson/immutable"
)

type pair struct {
	id  string
	val float64
}

// Handle No Confidence vote
func (a *AgentThree) HandleConfidencePoll(baseAgent agent.BaseAgent) decision.Intent {
	// decide whether to vote in the no-confidence vote based on personality
	toVote := rand.Intn(100)

	if toVote < a.personality {
		view := baseAgent.View()
		agentState := view.AgentState()
		ids := commons.ImmutableMapKeys(agentState)
		// extract agent ids paired with (reputation + social capital) score
		agentArray := make([]pair, 0, len(ids))
		for _, id := range ids {
			val := a.GetReputation(id) + float64(a.socialCap[id])
			agentArray = append(agentArray, pair{id, val})
		}
		// sort
		sort.Slice(agentArray, func(i, j int) bool {
			return agentArray[i].val > agentArray[j].val
		})
		var opinionArray []pair
		// extract top agents
		if len(agentArray) < 20 {
			opinionArray = agentArray
		} else {
			opinionArray = agentArray[0:20]
		}

		defectorCount := 0
		// did top agents defect?
		for _, pair := range opinionArray {
			a, _ := agentState.Get(pair.id)
			if a.Defector.IsDefector() {
				defectorCount++
			}
		}
		leaderRep := a.reputationMap[view.CurrentLeader()]
		leaderRepSwing := (leaderRep.Reputation - 30) / 10
		// Should leader reputation allow leaniency?
		voteNo := defectorCount - int(leaderRepSwing)
		// if over 50% of top agents defected, then vote no
		if voteNo > int((0.7 * float64(len(opinionArray)))) {
			return decision.Negative
		} else {
			return decision.Positive
		}
	} else {
		return decision.Abstain
	}
}

func (a *AgentThree) HandleElectionBallot(baseAgent agent.BaseAgent, param *decision.ElectionParams) decision.Ballot {

	// extract the name of the agents who have submitted manifestos
	candidateArray := make([]pair, 0, param.CandidateList().Len())
	iterator := param.CandidateList().Iterator()
	for !iterator.Done() {
		id, _, _ := iterator.Next()
		val := a.GetReputation(id) + float64(a.socialCap[id])
		candidateArray = append(candidateArray, pair{id, val})
	}
	// sort
	sort.Slice(candidateArray, func(i, j int) bool {
		return candidateArray[i].val > candidateArray[j].val
	})
	// should we vote?
	makeVote := rand.Intn(100)
	// if makeVote is lower than personality, then vote.
	if makeVote < a.personality {
		// Create Ballot
		var ballot decision.Ballot
		// number of manifesto preferences we are allowed
		numCandidate := int(param.NumberOfPreferences())
		if len(candidateArray) <= numCandidate {
			numCandidate = len(candidateArray)
		}
		for i := 0; i < numCandidate; i++ {
			ballot = append(ballot, candidateArray[i].id)
		}
		return ballot
	} else {
		// return an empty ballot (don't vote)
		var ballot decision.Ballot
		return ballot
	}
}

func (a *AgentThree) calcW1(state state.HiddenAgentState, id commons.ID) float64 {
	w1 := a.w1Map[id]
	currentHP := state.Hp
	currentStamina := state.Stamina
	prevHP := a.pastHPMap[id]
	prevStamina := a.pastStaminaMap[id]

	// extract and normalise personality (range[0,100]), use to dictate update step size
	personalityMod := float64(a.personality) / 100.0

	HP := prevHP - int(currentHP)
	stamina := prevStamina - int(currentStamina)

	// alg 6
	if stamina > 0 {
		w1 += 0.5 * personalityMod
	} else if stamina < 0 {
		w1 -= 0.5 * personalityMod
	}
	if HP > 0 {
		w1 += 0.5 * personalityMod
	} else if HP < 0 {
		w1 -= 0.5 * personalityMod
	}

	w1 = clampFloat(w1, 0.0, 10.0)

	return w1
}

func (a *AgentThree) calcW2(id commons.ID) float64 {
	w2 := a.w2Map[id]
	agentFought := false
	agentDefended := false
	nFD := 0
	numRounds := a.fightRoundsHistory.Len()

	// extract and normalise personality (range[0,100]), use to dictate update step size
	personalityMod := float64(a.personality) / 100.0

	// iterate over rounds of last level
	itr := a.fightRoundsHistory.Iterator()
	for !itr.Done() {
		res, _ := itr.Next()

		// search for agent in fight list and assign action
		agentFought = findAgentAction(res.AttackingAgents(), id)
		agentDefended = findAgentAction(res.ShieldingAgents(), id)

		if agentFought || agentDefended {
			nFD++
		}
	}
	// shifted to [-0.5, 0.5]
	ratioFD := float64(nFD) / float64(numRounds)
	w2 += (ratioFD - 0.5) * personalityMod

	w2 = clampFloat(w2, 0.0, 10.0)

	return w2
}

func (a *AgentThree) SocialCapital(baseAgent agent.BaseAgent) {
	view := baseAgent.View()
	agentState := view.AgentState()
	itr := agentState.Iterator()
	// use random Go iterators to select population up to sample limit
	count := 0

	for !itr.Done() {
		id, state, _ := itr.Next()
		defector := state.Defector
		if defector.IsDefector() {
			// punish defectors, and slightly reward cooperators
			a.socialCap[id] -= 2
		} else {
			a.socialCap[id] += 0.2
		}
		count++
		if count == (int(a.samplePercent * float64(a.numAgents))) {
			break
		}
	}
}

// func (a *AgentThree) Experience(baseAgent agent.BaseAgent) {
// 	view := baseAgent.View()
// 	agentState := view.AgentState()
// 	itr := agentState.Iterator()
// 	count := 0
// 	for !itr.Done() {
// 		id, state, _ := itr.Next()
// 		exp := state.LevelsAlive
// 		a.LevelsAlive[id] = int(exp)
// 		if count == (int(a.samplePercent * float64(a.numAgents))) {
// 			break
// 		}
// 	}

// }

func (a *AgentThree) Reputation(baseAgent agent.BaseAgent) {
	view := baseAgent.View()
	vAS := view.AgentState()

	ids := commons.ImmutableMapKeys(vAS)
	// get random shuffle of agent ids
	rand.Seed(time.Now().UnixNano())
	rand.Shuffle(len(ids), func(i, j int) { ids[i], ids[j] = ids[j], ids[i] })

	productivity := 5.0
	needs := 5.0

	// Number of agents to sample for KA (fixed)
	intendedSample := float64(a.numAgents) * a.samplePercent
	maxLength := float64(vAS.Len())
	sampleLength := int(math.Min(intendedSample, maxLength))
	cnt := 0

	// Use random access of maps in go to take n random samples
	for _, id := range ids {
		if cnt == sampleLength {
			// stop iterating when reaching the sample length
			return
		} else {
			hiddenState, _ := vAS.Get(id)

			// Init values on first access
			if _, ok := a.reputationMap[id]; !ok {
				// init weights to middle value
				a.InitRepWeights(baseAgent, id)
			}

			// Update values according to previous state
			a.w1Map[id] = a.calcW1(hiddenState, id)
			a.w2Map[id] = a.calcW2(id)

			// agent := a.reputationMap[id]

			// update reputation and experience
			a.reputationMap[id] = reputation{
				Reputation: a.w1Map[id]*needs + a.w2Map[id]*productivity,
				Experience: float64(hiddenState.LevelsAlive),
			}
			// agent.Reputation = a.w1Map[id]*needs + a.w2Map[id]*productivity

			// consider the agent's level
			// exp := hiddenState.LevelsAlive
			// agent.Experience = float64(exp)

			// Store this rounds values for the next one
			a.pastHPMap[id] = int(hiddenState.Hp)
			a.pastStaminaMap[id] = int(hiddenState.Stamina)
		}
		cnt++
	}
}

func (a *AgentThree) InitRepWeights(baseAgent agent.BaseAgent, id commons.ID) {
	view := baseAgent.View()
	vAS := view.AgentState()
	hiddenState, _ := vAS.Get(id)

	a.w1Map[id] = 5.0
	a.w2Map[id] = 5.0
	a.pastHPMap[id] = int(hiddenState.Hp)
	a.pastStaminaMap[id] = int(hiddenState.Stamina)
}

func (a *AgentThree) InitSocialCapital(baseAgent agent.BaseAgent) {
	view := baseAgent.View()
	agentState := view.AgentState()
	itr := agentState.Iterator()
	for !itr.Done() {
		id, _, _ := itr.Next()

		a.socialCap[id] = 25
	}
}

func findAgentAction(agentIDsMap immutable.List[commons.ID], ID commons.ID) bool {
	itr := agentIDsMap.Iterator()
	for !itr.Done() {
		_, actionAgentID := itr.Next()
		if actionAgentID == ID {
			return true
		}
	}
	return false
}
