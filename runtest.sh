# each el in list are params for a game
listAgentCollective=(30)
listAgentSelfish=(30)
listAgentAgr=(30)

listSELFISH_PER=(25)
listCOLLECTIVE_PER=(50)
listSELFLESS_PER=(75)

listDEFECTION=(true)
listUPDATE_PERSONALITY=(true)

for i in ${!listAgentCollective[@]}; do
  AgentCollective=${listAgentCollective[i]}
  AgentSelfish=${listAgentSelfish[i]}
  AgentAgr=${listAgentAgr[i]}

  AgentSELFISH_PER=${listSELFISH_PER[i]}
  AgentCOLLECTIVE_PER=${listCOLLECTIVE_PER[i]}
  AgentSELFLESS_PER=${listSELFLESS_PER[i]}

  AgentDEFECTION=${listDEFECTION[i]}
  AgentUPDATE_PERSONALITY=${listUPDATE_PERSONALITY[i]}
  
  export AGENT_COLLECTIVE_QUANTITY=$AgentCollective
  export AGENT_SELFLESS_QUANTITY=$AgentAgr
  export AGENT_SELFISH_QUANTITY=$AgentSelfish
 
  export SELFISH_PER=$AgentSELFISH_PER
  export COLLECTIVE_PER=$AgentCOLLECTIVE_PER
  export SELFLESS_PER=$AgentSELFLESS_PER

  export DEFECTION=$AgentDEFECTION
  export UPDATE_PERSONALITY=$AgentUPDATE_PERSONALITY

  OUTPUT=$(go run ./pkg/infra -fSanc=20 | tail -1)
  echo $OUTPUT
  python3 plotGame.py -f $OUTPUT

done
