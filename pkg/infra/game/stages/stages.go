package stages

import (
	"infra/config"
	"infra/game/agent"
	"infra/game/commons"
	"infra/game/decision"
	"infra/game/message"
	"infra/game/stage/fight"
	"infra/game/stage/initialise"
	"infra/game/stage/loot"
	"infra/game/stage/update"
	"infra/game/state"
	"infra/game/tally"
	"infra/logging"
	"time"

	"github.com/benbjohnson/immutable"
	//? Add you team folder like this:
	// t0 "infra/teams/team0"
	// t1 "infra/teams/team1"
)

// Mode ? Changed at compile time. eg change in .env to `MODE=0` to set this to '0'.
var Mode string

func ChooseDefaultStrategyMap(defaultStrategyMap map[commons.ID]func() agent.Strategy) map[commons.ID]func() agent.Strategy {
	switch Mode {
	// case "0":
	// 	return t0.InitAgentMap
	// case "1":
	// 	return t1.InitAgentMap
	default:
		return defaultStrategyMap
	}
}

func ChooseDefaultSurvivorStrategyMap(survivorStrategyMap map[commons.ID]func(personality uint, experience uint) agent.Strategy) map[commons.ID]func(personality uint, experience uint) agent.Strategy {
	switch Mode {
	// case "0":
	// 	return t0.InitSurvivorMap
	// case "1":
	// 	return t1.InitSurvivorMap
	default:
		return survivorStrategyMap
	}
}

func InitGameConfig() config.GameConfig {
	switch Mode {
	case "0":
		return initialise.InitGameConfig() // ? Can choose to just call the default function
	default:
		return initialise.InitGameConfig()
	}
}

func InitAgents(defaultStrategyMap map[commons.ID]func() agent.Strategy,
	defaultSurvivorStrategyMap map[commons.ID]func(personality uint, experience uint) agent.Strategy,
	gameConfig config.GameConfig,
	ptr *state.View,
	survivedAgentMap map[commons.ID]state.SurvivorAgentState,
) (numAgents uint, agentMap map[commons.ID]agent.Agent, agentStateMap map[commons.ID]state.AgentState, inventoryMap state.InventoryMap) {
	switch Mode {
	// case "0":
	// 	return t0.InitAgents(defaultStrategyMap, gameConfig, ptr)
	// case "1":
	// 	return t1.InitAgents(defaultStrategyMap, gameConfig, ptr)
	default:
		/*
			CHANGE HERE
		*/
		// return initialise.InitAgents(defaultStrategyMap, defaultSurvivorStrategyMap, gameConfig, ptr)
		return initialise.InitAgents(defaultStrategyMap, defaultSurvivorStrategyMap, gameConfig, ptr, survivedAgentMap)
	}
}

/*
Enter the code to create the survivor agent map here
*/
func InitSurvivorMap() map[commons.ID]state.SurvivorAgentState {
	survivorAgentMap := make(map[commons.ID]state.SurvivorAgentState)
	/*
		import the survivor agent file (importing a .json file)
		for each label in the dict (id) create a new key in the survivorAgentMap and assign the values from the dict
	*/
	start := config.EnvToBool("START", false)
	// if the start of the game, import surviviors
	if !start {
		logging.ImportSurvivors(survivorAgentMap)
	}
	// otherwise ignore
	return survivorAgentMap
}

func AgentLootDecisions(globalState state.State, availableLoot state.LootPool, agents map[commons.ID]agent.Agent, channelsMap map[commons.ID]chan message.TaggedMessage) *tally.Tally[decision.LootAction] {
	switch Mode {
	default:
		return loot.AgentLootDecisions(globalState, availableLoot, agents, channelsMap)
	}
}

func AgentFightDecisions(state state.State, agents map[commons.ID]agent.Agent, previousDecisions immutable.Map[commons.ID, decision.FightAction], channelsMap map[commons.ID]chan message.TaggedMessage) *tally.Tally[decision.FightAction] {
	switch Mode {
	// case "0":
	// 	//? Not necessary to use all function arguments
	// 	return t0.AllDefend(agents)
	default:
		return fight.AgentFightDecisions(state, agents, previousDecisions, channelsMap)
	}
}

func UpdateInternalStates(agentMap map[commons.ID]agent.Agent, globalState *state.State, immutableFightRounds *commons.ImmutableList[decision.ImmutableFightResult], votesResult *immutable.Map[decision.Intent, uint]) map[commons.ID]logging.AgentLog {
	switch Mode {
	// case "1":
	// 	return t1.UpdateInternalStates(agentMap, globalState, immutableFightRounds, votesResult)
	default:
		return update.UpdateInternalStates(agentMap, globalState, immutableFightRounds, votesResult)
	}
}

func UpdateLevelAlive(agentMap map[commons.ID]agent.Agent, globalState *state.State) {
	for id := range agentMap {
		agentState := globalState.AgentState[id]
		newLevel := agentState.LevelsAlive + 1
		globalState.AgentState[id] = state.AgentState{
			Hp:          agentState.Hp,
			Stamina:     agentState.Stamina,
			Attack:      agentState.Attack,
			Defense:     agentState.Defense,
			Weapons:     agentState.Weapons,
			Shields:     agentState.Shields,
			WeaponInUse: agentState.WeaponInUse,
			ShieldInUse: agentState.ShieldInUse,
			LevelsAlive: newLevel,
		}
	}
}

func HandleTrustStage(agentMap map[commons.ID]agent.Agent, channelsMap map[commons.ID]chan message.TaggedMessage) {
	closures := make(map[commons.ID]chan<- struct{})

	// SEND ALL MESSAGES OUT
	for _, a := range agentMap {
		msg := a.Strategy.CompileTrustMessage(agentMap)
		senderList := msg.Recipients

		for _, ag := range senderList {
			// fmt.Println("SENDING:")
			if a.ID() == ag {
				continue
			}
			a.SendBlockingMessage(ag, msg)
		}
	}

	for id, a := range agentMap {
		a := a
		closure := make(chan struct{})
		closures[id] = closure

		go (&a).HandleTrust(closure)
	}

	// timeout for agents to respond
	time.Sleep(25 * time.Millisecond)
	for _, closure := range closures {
		closure <- struct{}{}
		close(closure)
	}

	for _, c := range channelsMap {
		close(c)
	}
}

func AgentPruneMapping(agentMap map[commons.ID]agent.Agent, globalState *state.State) map[commons.ID]agent.Agent {
	leaderId := globalState.CurrentLeader
	leader, leaderIsAlive := agentMap[leaderId]

	if leaderIsAlive {
		prunedMap := leader.PruneAgentList(agentMap)
		prunedMap[leaderId] = leader

		return prunedMap
	}
	// leader has died, hence no sanctioning
	return agentMap

}

func AgentMapToSortedArray(prunedMap map[commons.ID]agent.Agent, globalState *state.State) []agent.Agent {
	leaderId := globalState.CurrentLeader
	leader, leaderIsAlive := prunedMap[leaderId]

	if leaderIsAlive {
		prunedArray := leader.SortAgentsArray(prunedMap)
		return prunedArray
	}

	defaultArray := make([]agent.Agent, len(prunedMap))

	idx := 0
	for _, ag := range prunedMap {
		defaultArray[idx] = ag
		idx++
	}
	return defaultArray
}

/*
	Agent map to suvirors map for storage
*/

func AgentMapToSurvivorMap(agentMap map[commons.ID]agent.Agent) map[commons.ID]state.SurvivorAgentState {
	survivorMap := make(map[commons.ID]state.SurvivorAgentState)
	for id, agent := range agentMap {
		personality, _ := agent.GetStats()
		Hp := agent.AgentState().Hp
		Stamina := agent.AgentState().Stamina
		LevelsAlive := agent.AgentState().LevelsAlive
		survivorMap[id] = state.SurvivorAgentState{
			Hp:          Hp,
			Stamina:     Stamina,
			Personality: personality,
			LevelsAlive: LevelsAlive,
		}
	}
	return survivorMap
}
