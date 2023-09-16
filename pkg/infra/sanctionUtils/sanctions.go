package sanctions

import "infra/game/commons"

type SanctionActivity struct {
	sanctionActive bool
	duration       int
}

func (s *SanctionActivity) MakeSanction(length int) {
	s.sanctionActive = true
	s.duration = length
	if length == 0 {
		s.sanctionActive = false
	}
}

func (s *SanctionActivity) AgentIsSanctioned() bool {
	return s.sanctionActive
}

func (s *SanctionActivity) UpdateSanction() {
	if !s.sanctionActive {
		return
	}

	if s.duration > 0 {
		s.duration--
	}
	if s.duration == 0 {
		s.sanctionActive = false
	}

}

var GlobalSanctionMap map[commons.ID]SanctionActivity = make(map[commons.ID]SanctionActivity)
var GlobalSanctionHistory map[commons.ID]([]int) = make(map[commons.ID]([]int))
