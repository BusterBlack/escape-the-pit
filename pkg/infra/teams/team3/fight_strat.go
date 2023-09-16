package team3

import (
	"math/rand"

	"infra/game/agent"
	"infra/game/commons"
	"infra/game/decision"
	"infra/game/message"
	"infra/game/message/proposal"

	"github.com/benbjohnson/immutable"
)

var (
	initHP        int
	initMonsterHP int
)

// HP pool donation
func (a *AgentThree) DonateToHpPool(baseAgent agent.BaseAgent) uint {
	// AS := baseAgent.AgentState()
	// donation := rand.Intn(2)
	// // If our health is > 50% and we feel generous then donate some (max 20%) HP
	// if donation == 1 {
	// 	if int(AS.Hp) > int(0.8*float64(GetStartingHP())) {
	// 		return uint(rand.Intn((int(AS.Hp) * 30)) / 100)
	// 	} else if int(AS.Hp) > int(0.5*float64(GetStartingHP())) {
	// 		return uint(rand.Intn((int(AS.Hp) * 10)) / 100)
	// 	} else {
	// 		return 0
	// 	}
	// } else {
	// 	return 0
	// }
	return 0
}

func (a *AgentThree) FightAction(
	baseAgent agent.BaseAgent,
	proposedAction decision.FightAction,
	acceptedProposal message.Proposal[decision.FightAction],
) decision.FightAction {
	disobey := rand.Intn(100)
	// if disobey value is lower than personality then do not defect
	// lower personality values mean more selfish (therefore more likely to defect)
	if disobey < (a.personality - ((a.experience / 40) * 5)) {
		return proposedAction
	} else {
		return a.FightActionNoProposal(baseAgent)
	}
}

func (a *AgentThree) FightActionNoProposal(baseAgent agent.BaseAgent) decision.FightAction {
	agentState := baseAgent.AgentState()
	// alg 8
	if float64(agentState.Hp) < 1.05*AverageArray(GetHealthAllAgents(baseAgent)) || float64(agentState.Stamina) < 1.05*AverageArray(GetStaminaAllAgents(baseAgent)) {
		return decision.Cower
	} else if agentState.BonusDefense() <= agentState.BonusAttack() {
		return decision.Attack
	} else {
		return decision.Defend
	}
}

// Send proposal to leader
func (a *AgentThree) HandleFightInformation(m message.TaggedInformMessage[message.FightInform], baseAgent agent.BaseAgent, fightactionMap *immutable.Map[commons.ID, decision.FightAction]) {
	id := baseAgent.ID()
	choice, _ := fightactionMap.Get(id)
	thresholdValues := a.thresholdDecision(baseAgent, choice)
	// fmt.Println(m)

	// should i make a proposal (based on personality)
	makesProposal := rand.Intn(100)
	// if makesProposal is lower than personality, then make proposal
	// low personality scores mean more selfish,
	if makesProposal < a.personality {
		rules := make([]proposal.Rule[decision.FightAction], 0)

		// fight rule HT AND ST condition
		rules = append(rules, *proposal.NewRule(decision.Attack,
			proposal.NewAndCondition(*proposal.NewComparativeCondition(proposal.Health, proposal.GreaterThan, uint(thresholdValues.Health)),
				*proposal.NewComparativeCondition(proposal.Stamina, proposal.GreaterThan, uint(thresholdValues.Stamina))),
		))
		// fight rule ATT condition
		rules = append(rules, *proposal.NewRule(decision.Attack,
			proposal.NewComparativeCondition(proposal.TotalAttack, proposal.GreaterThan, uint(thresholdValues.Attack)),
		))
		// defend rule HP AND ST condition
		rules = append(rules, *proposal.NewRule(decision.Defend,
			proposal.NewAndCondition(*proposal.NewComparativeCondition(proposal.Health, proposal.GreaterThan, uint(thresholdValues.Health)),
				*proposal.NewComparativeCondition(proposal.Stamina, proposal.GreaterThan, uint(thresholdValues.Stamina))),
		))
		// defend rule DEF condition
		rules = append(rules, *proposal.NewRule(decision.Defend,
			proposal.NewComparativeCondition(proposal.TotalDefence, proposal.GreaterThan, uint(thresholdValues.Defence)),
		))
		// COWER condition (as low as possible)
		rules = append(rules, *proposal.NewRule(decision.Cower,
			proposal.NewComparativeCondition(proposal.Health, proposal.GreaterThan, 1),
		))

		prop := *commons.NewImmutableList(rules)
		_ = baseAgent.SendFightProposalToLeader(prop)
	}
}

// Calculate our agents action
func (a *AgentThree) CurrentAction(baseAgent agent.BaseAgent) decision.FightAction {
	view := baseAgent.View()
	agentState := baseAgent.AgentState()

	currentLevel := int(view.CurrentLevel())
	var attackDealt int
	// only sample at start
	if currentLevel == 1 {
		initHP = int(agentState.Hp)
		initMonsterHP = int(view.MonsterHealth())
	}
	// edge case - alg 9
	if float64(agentState.Hp) < 0.6*AverageArray(GetHealthAllAgents(baseAgent)) || float64(agentState.Stamina) < 0.6*AverageArray(GetStaminaAllAgents(baseAgent)) {
		return decision.Cower
	}
	// change decision, already not edge case - alg 10
	// every 3 levels, alpha +1, alpha init at 3
	alpha := (currentLevel / 3) + 3

	if currentLevel > alpha+3 {
		damageTaken := initHP - int(agentState.Hp)
		if initMonsterHP == 0 {
			attackDealt = 0
		} else {
			attackDealt = (initMonsterHP - int(view.MonsterHealth())) / initMonsterHP
		}

		// re-init vars
		initHP = int(agentState.Hp)
		initMonsterHP = int(view.MonsterHealth())

		if attackDealt <= damageTaken {
			return decision.Attack
		} else if attackDealt > damageTaken {
			return decision.Defend
		}
	}
	// catchall
	return decision.Attack
}

// Vote on proposal
func (a *AgentThree) HandleFightProposal(m message.Proposal[decision.FightAction], baseAgent agent.BaseAgent) decision.Intent {
	// determine whether to vote based on personality.
	intent := rand.Intn(100)

	// rules := m.Rules()
	// itr := rules.Iterator()
	// for !itr.Done() {
	// 	rule, _ := itr.Next()
	// 	// baseAgent.Log(logging.Trace, logging.LogField{"rule": rule}, "Rule Proposal")
	// }

	// if the intent is less than personality, then decide vote action
	if intent < a.personality {
		// calculate vote action
		return decision.Positive
	} else {
		// can we abstain from this vote?
		return decision.Abstain
	}
}

func (a *AgentThree) thresholdDecision(baseAgent agent.BaseAgent, choice decision.FightAction) thresholdVals {
	var thresholds thresholdVals
	// initiate modifers
	alpha := 0.2
	beta := 0.1
	// get my stats
	myStats := a.getMyStats(baseAgent)
	// get group stats
	groupAvStats := a.getGroupAvStats(baseAgent)

	// get differences (group to me)
	Delta1HP := groupAvStats.Health - float64(myStats.Health)
	Delta1ST := groupAvStats.Stamina - float64(myStats.Stamina)
	Delta1ATT := groupAvStats.Attack - float64(myStats.Attack)
	Delta1DEF := groupAvStats.Defence - float64(myStats.Defence)

	if len(a.TSN) > 0 {
		// get TSN average stats
		TSNavStats := a.getTSNAvStats(baseAgent)
		// get differences (group to TSN)
		Delta2HP := groupAvStats.Health - TSNavStats.Health
		Delta2ST := groupAvStats.Stamina - TSNavStats.Stamina
		Delta2ATT := groupAvStats.Attack - TSNavStats.Attack
		Delta2DEF := groupAvStats.Defence - TSNavStats.Defence

		thresholds.Health = myStats.Health + alpha*Delta1HP + beta*Delta2HP
		thresholds.Stamina = myStats.Stamina + alpha*Delta1ST + beta*Delta2ST
		thresholds.Attack = myStats.Attack + alpha*Delta1ATT + beta*Delta2ATT
		thresholds.Defence = myStats.Defence + alpha*Delta1DEF + beta*Delta2DEF

		return thresholds
	}
	// caluclate the thresholds (for all the decisions)
	thresholds.Health = (myStats.Health + alpha*Delta1HP) * float64(0.98)
	thresholds.Stamina = (myStats.Stamina + alpha*Delta1ST) * float64(0.98)
	thresholds.Attack = (myStats.Attack + alpha*Delta1ATT) * float64(0.98)
	thresholds.Defence = (myStats.Defence + alpha*Delta1DEF) * float64(0.98)

	return thresholds
}

func (a *AgentThree) HandleUpdateWeapon(baseAgent agent.BaseAgent) decision.ItemIdx {
	// weapons := b.AgentState().Weapons
	// return decision.ItemIdx(rand.Intn(weapons.Len() + 1))

	// 0th weapon has greatest attack points
	return decision.ItemIdx(0)
}

func (a *AgentThree) HandleUpdateShield(baseAgent agent.BaseAgent) decision.ItemIdx {
	// shields := b.AgentState().Shields
	// return decision.ItemIdx(rand.Intn(shields.Len() + 1))
	return decision.ItemIdx(0)
}
