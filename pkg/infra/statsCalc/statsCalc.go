package statscalc

import (
	"infra/game/agent"

	"gonum.org/v1/gonum/stat"
)

type Metric int

const (
	ATK Metric = iota
	DEF
	HP
	STAM
)

type StatsCalc struct {
	data map[string]agent.Agent
}

func MakeStatsCalc(inputData map[string]agent.Agent) *StatsCalc {
	return &StatsCalc{data: inputData}
}

func (s *StatsCalc) SetStatsCalcData(inputData map[string]agent.Agent) {
	s.data = inputData
}

func (s *StatsCalc) selectStat(m Metric) []float64 {
	output := make([]float64, len(s.data))

	idx := 0
	for _, ag := range s.data {
		var addedData float64
		state := ag.AgentState()
		switch m {
		case ATK:
			addedData = float64(state.TotalAttack())
		case DEF:
			addedData = float64(state.TotalDefense())
		case HP:
			addedData = float64(state.Hp)
		case STAM:
			addedData = float64(state.Stamina)
		default:
			addedData = float64(state.Hp)
		}
		output[idx] = addedData
		idx++
	}
	return output
}

func (s *StatsCalc) GetMean(m Metric) float64 {
	meanArray := s.selectStat(m)
	return stat.Mean(meanArray, nil)
}

func (s *StatsCalc) GetVar(m Metric) float64 {
	varArray := s.selectStat(m)
	return stat.Mean(varArray, nil)
}

func (s *StatsCalc) GetStdDev(m Metric) float64 {
	stArray := s.selectStat(m)
	return stat.StdDev(stArray, nil)
}

var Calc StatsCalc = StatsCalc{}
