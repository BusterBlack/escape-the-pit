package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"os"
	"path"
	"sort"
	"strconv"
	"time"

	"github.com/google/uuid"

	"infra/config"
	"infra/game/agent"
	"infra/game/commons"
	"infra/game/decision"
	gamemath "infra/game/math"
	"infra/game/message"
	"infra/game/stage/election"
	"infra/game/stage/fight"
	"infra/game/stages"
	"infra/game/state"
	"infra/logging"

	"github.com/benbjohnson/immutable"
	"github.com/joho/godotenv"
	"golang.org/x/exp/constraints"
)

/*
	Package Variables
*/

var (
	viewPtr     = &state.View{}
	globalState *state.State
	agentMap    map[commons.ID]agent.Agent
	gameConfig  *config.GameConfig
)

/*
	Init Helpers
*/

func updateView(ptr *state.View, globalState *state.State) {
	*ptr = globalState.ToView()
}

func initGame() {
	if godotenv.Load() != nil {
		logging.Log(logging.Error, nil, "No .env file located, using defaults")
	}

	stages.Mode = config.EnvToString("MODE", "default")

	initGameConfig := stages.InitGameConfig()
	gameConfig = &initGameConfig
	defStrategyMap := stages.ChooseDefaultStrategyMap(InitAgentMap)
	defSurvivorStrategyMap := stages.ChooseDefaultSurvivorStrategyMap(InitSurvivorMap)
	/*
		Here enter the call to the function to extract the survivor agent map and assign
	*/
	survivedAgentMap := stages.InitSurvivorMap()
	/*
		CHANGE HERE
	*/
	// numAgents, agents, agentStateMap, inventoryMap := stages.InitAgents(defStrategyMap, defSurvivorStrategyMap, initGameConfig, viewPtr)
	numAgents, agents, agentStateMap, inventoryMap := stages.InitAgents(defStrategyMap, defSurvivorStrategyMap, initGameConfig, viewPtr, survivedAgentMap)
	gameConfig.InitialNumAgents = numAgents

	globalState = &state.State{
		MonsterHealth: gamemath.CalculateMonsterHealth(gameConfig.InitialNumAgents, gameConfig.Stamina, gameConfig.NumLevels, 1),
		MonsterAttack: gamemath.CalculateMonsterDamage(gameConfig.InitialNumAgents, gameConfig.StartingHealthPoints, gameConfig.Stamina, gameConfig.ThresholdPercentage, gameConfig.NumLevels, 1),
		AgentState:    agentStateMap,
		InventoryMap:  inventoryMap,
		Defection:     gameConfig.Defection,
	}
	agentMap = agents
}

/*
	Communication Helpers
*/

func addCommsChannels() map[commons.ID]chan message.TaggedMessage {
	keys := make([]commons.ID, len(agentMap))
	res := make(map[commons.ID]chan message.TaggedMessage)
	i := 0
	for k := range agentMap {
		keys[i] = k
		i++
	}

	for _, key := range keys {
		res[key] = make(chan message.TaggedMessage, 100)
	}
	immutableMap := createImmutableMapForChannels(res)
	for id, a := range agentMap {
		a.SetCommunication(agent.NewCommunication(res[id], *immutableMap.Delete(id)))
	}
	return res
}

func createImmutableMapForChannels[K constraints.Ordered, V any](peerChannels map[K]chan V) immutable.Map[K, chan<- V] {
	builder := immutable.NewMapBuilder[K, chan<- V](nil)
	for pID, channel := range peerChannels {
		builder.Set(pID, channel)
	}
	return *builder.Map()
}

/*
	Election Helpers
*/

func runElection() uint {
	electedAgent, manifesto := election.HandleElection(globalState, agentMap, decision.VotingStrategy(gameConfig.VotingStrategy), gameConfig.VotingPreferences)
	termLeft := manifesto.TermLength()
	globalState.LeaderManifesto = manifesto
	globalState.CurrentLeader = electedAgent
	updateView(viewPtr, globalState)
	return termLeft
}

func runConfidenceVote(termLeft uint) (uint, map[decision.Intent]uint) {
	votes := make(map[decision.Intent]uint)
	for _, a := range agentMap {
		votes[a.Strategy.HandleConfidencePoll(*a.BaseAgent)]++
	}
	leader := agentMap[globalState.CurrentLeader]
	leaderName := leader.BaseAgent.Name()

	logging.Log(logging.Info, logging.LogField{
		"positive":  votes[decision.Positive],
		"negative":  votes[decision.Negative],
		"abstain":   votes[decision.Abstain],
		"threshold": globalState.LeaderManifesto.OverthrowThreshold(),
		"leader":    globalState.CurrentLeader,
		"team":      leaderName,
	}, "Confidence Vote")

	if votes[decision.Negative]+votes[decision.Positive] == 0 {
		return termLeft, votes
	} else if 100*votes[decision.Negative]/(votes[decision.Negative]+votes[decision.Positive]) > globalState.LeaderManifesto.OverthrowThreshold() {
		logging.Log(logging.Info, nil, fmt.Sprintf("%s got ousted", globalState.CurrentLeader))
		termLeft = runElection()
		// log the results of the new election
		// fmt.Println("Current Leader Shit -------------------")
		// fmt.Println(agentMap[globalState.CurrentLeader])
		// fmt.Println(agentMap[globalState.CurrentLeader].BaseAgent.ID())
		// fmt.Println(agentMap[globalState.CurrentLeader].BaseAgent.Name())

		levelLog := logging.LevelStages{}
		levelLog.ElectionStage = logging.ElectionStage{
			Occurred: true,
			Winner:   globalState.CurrentLeader,
			Team:     agentMap[globalState.CurrentLeader].BaseAgent.Name(),
			Manifesto: logging.ManifestoLog{
				FightImposition:     globalState.LeaderManifesto.FightDecisionPower(),
				LootImposition:      globalState.LeaderManifesto.LootDecisionPower(),
				TermLength:          globalState.LeaderManifesto.TermLength(),
				ThresholdPercentage: globalState.LeaderManifesto.OverthrowThreshold(),
			},
		}
		logging.Log(logging.Info, logging.LogField{
			"Fight Imp": globalState.LeaderManifesto.FightDecisionPower(),
			"Loot Imp":  globalState.LeaderManifesto.LootDecisionPower(),
			"Term":      globalState.LeaderManifesto.TermLength(),
			"Threshold": globalState.LeaderManifesto.OverthrowThreshold(),
			"Winner":    globalState.CurrentLeader,
			"Team":      agentMap[globalState.CurrentLeader].BaseAgent.Name(),
		}, "Re-Election Vote")
	}
	return termLeft, votes
}

/*
	Fight Helpers
*/

func damageCalculation(fightRoundResult decision.FightResult) {
	if len(fightRoundResult.CoweringAgents) != len(agentMap) {
		globalState.MonsterHealth = commons.SaturatingSub(globalState.MonsterHealth, fightRoundResult.AttackSum)
		if globalState.MonsterHealth > 0 && fightRoundResult.ShieldSum < globalState.MonsterAttack {
			agentsFighting := append(fightRoundResult.AttackingAgents, fightRoundResult.ShieldingAgents...)
			damageTaken := globalState.MonsterAttack - fightRoundResult.ShieldSum
			fight.DealDamage(damageTaken, agentsFighting, agentMap, globalState)
			// TODO: Monster disruptive ability
		}
	} else {
		damageTaken := globalState.MonsterAttack
		fight.DealDamage(damageTaken, fightRoundResult.CoweringAgents, agentMap, globalState)
	}
	*viewPtr = globalState.ToView()
}

/*
	Hp Pool Helpers
*/

func checkHpPool() bool {
	if globalState.HpPool >= globalState.MonsterHealth {
		logging.Log(logging.Info, logging.LogField{
			"Original HP Pool":  globalState.HpPool,
			"Monster Health":    globalState.MonsterHealth,
			"HP Pool Remaining": globalState.HpPool - globalState.MonsterHealth,
		}, fmt.Sprintf("Skipping level %d through HP Pool", globalState.CurrentLevel))

		globalState.HpPool -= globalState.MonsterHealth
		globalState.MonsterHealth = 0
		return true
	}
	return false
}

func statDelta() float64 {
	rand.Seed(time.Now().UnixNano())
	min := 0.8
	max := 1.2
	return min + rand.Float64()*(max-min)
}

func generateLootPool(numAgents uint) *state.LootPool {
	nWeapons, nShields := gamemath.GetEquipmentDistribution(numAgents)
	nHealthPotions, nStaminaPotions := gamemath.GetPotionDistribution(numAgents)

	makeItems := func(nItems uint, stats uint, itemType state.ItemName) *commons.ImmutableList[state.Item] {
		items := make([]state.Item, nItems)
		for i := uint(0); i < nItems; i++ {
			delta := statDelta()
			items[i] = *state.NewItem(uuid.NewString(), uint(float64(stats)*delta), itemType)
		}
		sort.SliceStable(items, func(i, j int) bool {
			return items[i].Value() > items[j].Value()
		})
		return commons.NewImmutableList(items)
	}

	recalculatedMonsterHealth := gamemath.CalculateMonsterHealth(gameConfig.InitialNumAgents, gameConfig.Stamina, gameConfig.NumLevels, globalState.CurrentLevel)

	return state.NewLootPool(
		// Weapons
		makeItems(nWeapons, gamemath.GetWeaponDamage(recalculatedMonsterHealth, numAgents), state.SWORD),
		// Shields
		makeItems(nShields, gamemath.GetShieldProtection(globalState.MonsterAttack, numAgents), state.SHIELD),
		// Health Potions
		makeItems(nHealthPotions, gamemath.GetHealthPotionValue(globalState.MonsterAttack, numAgents), state.HP_POTION),
		// Stamina Potions
		makeItems(nStaminaPotions, gamemath.GetStaminaPotionValue(recalculatedMonsterHealth, numAgents), state.STAMINA_POTION),
	)
}

func uintStr(in uint) string {
	return strconv.Itoa(int(in))
}

/*
	Output Helpers
*/

func OutputAgentMap(survivors map[commons.ID]state.SurvivorAgentState) {
	jsonBuf, err := json.MarshalIndent(survivors, "", "\t")
	if err != nil {
		log.Fatalf("Failed to Marshal gameStates: %v", err)
		return
	}

	wd, err := os.Getwd()
	if err != nil {
		log.Fatalf("Failed to get working directory: %v", err)
		return
	}

	outputDir := path.Join(wd, "output/survivors.json")

	err = os.WriteFile(outputDir, jsonBuf, 0777)
	if err != nil {
		log.Fatalf("Failed to write agentMap to file: %v", err)
		return
	}
}

/*
	CSV Logging Help
*/

func initCsvLogging() (*csv.Writer, *os.File) {
	// create csv for logging

	csvFile, err := os.Create("logCSV/gameLog.csv")
	if err != nil {
		log.Fatalf("failed creating file: %s", err)
	}

	w := csv.NewWriter(csvFile)
	// title row
	firstRow := []string{"level", "total agents alive", "average health", "average stamina", "average attack", "average defense", "average personality", "average sanctioned", "count selfless", "count selfish", "count collective"}
	if err := w.Write(firstRow); err != nil {
		log.Fatalln("error writing record to file", err)
	}
	secondRow := []string{"0", "90", "1000", "2000", "20", "20", "50", "0", "30", "30", "30"}
	if err := w.Write(secondRow); err != nil {
		log.Fatalln("error writing zeroth level to file", err)
	}
	return w, csvFile
}
func logLevel(levelLog logging.LevelStages, agentmap map[string]agent.Agent, w *csv.Writer) {

	// quantize personalities to count them
	countSelfless := 0
	countSelfish := 0
	countCollective := 0
	avPersonality := 0
	avSanctioned := 0
	for _, a := range agentMap {
		personality, sanctioned := a.GetStats()
		avPersonality += personality
		avSanctioned += sanctioned
		if personality <= 25 {
			countSelfish += 1
		} else if personality >= 75 {
			countSelfless += 1
		} else {
			countCollective += 1
		}

	}
	countAgentint := len(agentMap)
	if countAgentint > 0 {
		avPersonality /= countAgentint
		avSanctioned /= countAgentint
	}

	lvStats := levelLog.LevelStats
	row := []string{uintStr(lvStats.CurrentLevel),
		uintStr(lvStats.NumberOfAgents),
		uintStr(lvStats.AverageAgentHealth),
		uintStr(lvStats.AverageAgentStamina),
		uintStr(lvStats.AverageAgentAttack),
		uintStr(lvStats.AverageAgentShield),
		strconv.Itoa(avPersonality),
		strconv.Itoa(avSanctioned),
		strconv.Itoa(countSelfless),
		strconv.Itoa(countSelfish),
		strconv.Itoa(countCollective),
	}
	if err := w.Write(row); err != nil {
		log.Fatalln("error writing record to file", err)
	}

	w.Flush()
}

func LogTracking(agentMap map[string]agent.Agent, trackLog *logging.TrackLog, fightActions decision.FightResult, prunedAgentMap map[commons.ID]agent.Agent) {
	for id, a := range agentMap {
		log := trackLog.Agents[id]
		state := a.AgentState()
		defector := a.AgentState().Defector
		Personality, _ := a.GetStats()
		var sanctioned int
		if _, ok := prunedAgentMap[id]; ok {
			sanctioned = 0
		} else {
			sanctioned = 1
		}

		trackLog.Agents[id] = logging.AgentTrack{
			FightAction: append(log.FightAction, uint(fightActions.Choices[id])),
			Hp:          append(log.Hp, a.AgentState().Hp),
			Stamina:     append(log.Stamina, a.AgentState().Stamina),
			Attack:      append(log.Attack, state.TotalAttack()),
			Defense:     append(log.Defense, state.TotalDefense()),
			LevelsAlive: append(log.LevelsAlive, a.AgentState().LevelsAlive),
			TSNlength:   append(log.TSNlength, uint(len(a.GetTSN()))),
			Personality: append(log.Personality, uint(Personality)),
			// Sanctioned:  append(log.Sanctioned, defector.IsDefector()),
			Defector:   append(log.Defector, defector.IsDefector()),
			Sanctioned: append(log.Sanctioned, sanctioned),
		}
	}
}
