package logging

import (
	"encoding/json"
	"infra/game/commons"
	"os"
	"path"
)

var fileTrack TrackLog

type AgentTrack struct {
	FightAction []uint
	Hp          []uint
	Stamina     []uint
	Attack      []uint
	Defense     []uint
	LevelsAlive []uint
	Personality []uint
	Sanctioned  []int
	TSNlength   []uint
	Defector    []bool
}

type TrackLog struct {
	Agents map[commons.ID]AgentTrack
}

/*
Track to file function to add to the track log
Assigning the track in the mian file
output track log using new output functin
*/
func TrackLogToFile(trackLog TrackLog) {
	fileTrack = trackLog
}

func OutputTrackLog() {
	trackLogJSON, err := json.MarshalIndent(fileTrack, "", "    ")
	if err != nil {
		log.Fatalf("Fail to Marshal track log: %v", err)
		return
	}

	wd, err := os.Getwd()
	if err != nil {
		log.Fatalf("Failed to get working Directory: %v", err)
		return
	}

	outputDir := path.Join(wd, "output/track.json")

	err = os.WriteFile(outputDir, trackLogJSON, 0777)
	if err != nil {
		log.Fatalf("Failed to write file: %v", err)
		return
	}

}
