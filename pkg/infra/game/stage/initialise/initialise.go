package initialise

import (
	"infra/config"
	"infra/game/agent"
	"infra/game/commons"
	"infra/game/state"

	"github.com/benbjohnson/immutable"
	"github.com/google/uuid"
)

func InstantiateAgent[S agent.Strategy](gameConfig config.GameConfig,
	agentMap map[commons.ID]agent.Agent,
	agentStateMap map[commons.ID]state.AgentState,
	quantity uint,
	strategyConstructor func() S,
	agentName string,
	viewPtr *state.View,
) {
	for i := uint(0); i < quantity; i++ {
		agentID := uuid.NewString()
		agentMap[agentID] = agent.Agent{
			BaseAgent: agent.NewBaseAgent(nil, agentID, agentName, viewPtr),
			Strategy:  strategyConstructor(),
		}

		agentStateMap[agentID] = state.AgentState{
			Hp:          gameConfig.StartingHealthPoints,
			Stamina:     gameConfig.Stamina,
			Attack:      gameConfig.StartingAttackStrength,
			Defense:     gameConfig.StartingShieldStrength,
			Weapons:     *immutable.NewList[state.Item](),
			Shields:     *immutable.NewList[state.Item](),
			WeaponInUse: uuid.Nil.String(),
			ShieldInUse: uuid.Nil.String(),
			LevelsAlive: uint(0),
		}
	}
}

func InstantiateSurvivedAgent[S agent.Strategy](gameConfig config.GameConfig,
	agentMap map[commons.ID]agent.Agent,
	agentStateMap map[commons.ID]state.AgentState,
	survivedAgentMap map[commons.ID]state.SurvivorAgentState,
	strategyConstructor func(personality uint, experience uint) S,
	agentName string,
	viewPtr *state.View,
) {
	// grab agent ID
	for Id, s := range survivedAgentMap {
		/*
			here the survivedAgentMap needs to be map[commons.ID]state.SurvivedAgentState
			Therefore need to make a new state type for the survived agent state
			And then create the new map from the suriving agent file.
			To do this, we need to extract the file data and use it to create the new map
		*/
		agentID := Id
		agentMap[agentID] = agent.Agent{
			BaseAgent: agent.NewBaseAgent(nil, agentID, agentName, viewPtr),
			// Strategy:  strategyConstructor(uint(s.Personality)),
			Strategy: strategyConstructor(uint(s.Personality), uint(s.LevelsAlive)),
		}

		agentStateMap[agentID] = state.AgentState{
			Hp:          s.Hp,
			Stamina:     s.Stamina,
			Attack:      gameConfig.StartingAttackStrength,
			Defense:     gameConfig.StartingShieldStrength,
			Weapons:     *immutable.NewList[state.Item](),
			Shields:     *immutable.NewList[state.Item](),
			WeaponInUse: uuid.Nil.String(),
			ShieldInUse: uuid.Nil.String(),
			LevelsAlive: s.LevelsAlive,
		}
	}
}

func InitGameConfig() config.GameConfig {
	gameConfig := config.GameConfig{
		NumLevels:              config.EnvToUint("LEVELS", 60),
		StartingHealthPoints:   config.EnvToUint("STARTING_HP", 1000),
		StartingAttackStrength: config.EnvToUint("STARTING_ATTACK", 20),
		StartingShieldStrength: config.EnvToUint("STARTING_SHIELD", 20),
		ThresholdPercentage:    config.EnvToFloat("THRESHOLD_PCT", 0.01),
		InitialNumAgents:       uint(0),
		Stamina:                config.EnvToUint("BASE_STAMINA", 2000),
		VotingStrategy:         config.EnvToUint("VOTING_STRATEGY", 0),
		VotingPreferences:      config.EnvToUint("VOTING_PREFERENCES", 2),
		Defection:              config.EnvToBool("DEFECTION", true),
	}

	return gameConfig
}

func InitAgents(
	defaultStrategyMap map[commons.ID]func() agent.Strategy,
	defaultSurvivorStrategyMap map[commons.ID]func(personality uint, experience uint) agent.Strategy,
	gameConfig config.GameConfig,
	ptr *state.View,
	survivedAgentMap map[commons.ID]state.SurvivorAgentState,
	//
) (numAgents uint, agentMap map[commons.ID]agent.Agent, agentStateMap map[commons.ID]state.AgentState, inventoryMap state.InventoryMap) {
	agentMap = make(map[commons.ID]agent.Agent)
	agentStateMap = make(map[commons.ID]state.AgentState)
	inventoryMap = state.InventoryMap{
		Weapons: make(map[commons.ItemID]uint),
		Shields: make(map[commons.ItemID]uint),
	}

	numAgents = 0

	for agentName, strategy := range defaultStrategyMap {
		expectedEnvName := "AGENT_" + agentName + "_QUANTITY"
		quantity := config.EnvToUint(expectedEnvName, 30)

		numAgents += quantity
		InstantiateAgent(gameConfig, agentMap, agentStateMap, quantity, strategy, agentName, ptr)
	}
	/*
		get START values from .env file
		if the value is true... add surviving agents to map
		otherwise skip
	*/
	start := config.EnvToBool("START", true)
	if !start {
		for agentName, strategy := range defaultSurvivorStrategyMap {
			numAgents += uint(len(survivedAgentMap))
			InstantiateSurvivedAgent(gameConfig, agentMap, agentStateMap, survivedAgentMap, strategy, agentName, ptr)
		}
	}

	return
}
