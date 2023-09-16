package cmdline

type CmdLine struct {
	FixedSanctionDuration        int
	MaxGraduatedSanctionDuration int
	DynamicSanctions             bool
	GraduatedSanctions           bool
	PersistentSanctions          bool
}

var CmdLineInits CmdLine = CmdLine{}
