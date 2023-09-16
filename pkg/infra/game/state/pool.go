package state

import (
	"infra/game/commons"
)

type ItemName string

const (
	SWORD          ItemName = "Sword"
	SHIELD         ItemName = "Shield"
	HP_POTION      ItemName = "HP_Potion"
	STAMINA_POTION ItemName = "Stamina_Potion"
	NULL           ItemName = "Null"
)

type Item struct {
	id    commons.ItemID
	value uint
	name  ItemName
}

func (i Item) Id() commons.ItemID {
	return i.id
}

func (i Item) Value() uint {
	return i.value
}

func (i Item) Name() ItemName {
	return i.name
}

func NewItem(id commons.ItemID, value uint, name ItemName) *Item {
	return &Item{id: id, value: value, name: name}
}

type LootPool struct {
	weapons        *commons.ImmutableList[Item]
	shields        *commons.ImmutableList[Item]
	hpPotions      *commons.ImmutableList[Item]
	staminaPotions *commons.ImmutableList[Item]
}

func (l LootPool) Weapons() *commons.ImmutableList[Item] {
	return l.weapons
}

func (l LootPool) Shields() *commons.ImmutableList[Item] {
	return l.shields
}

func (l LootPool) HpPotions() *commons.ImmutableList[Item] {
	return l.hpPotions
}

func (l LootPool) StaminaPotions() *commons.ImmutableList[Item] {
	return l.staminaPotions
}

func NewLootPool(weapons *commons.ImmutableList[Item], shields *commons.ImmutableList[Item], hpPotions *commons.ImmutableList[Item], staminaPotions *commons.ImmutableList[Item]) *LootPool {
	return &LootPool{weapons: weapons, shields: shields, hpPotions: hpPotions, staminaPotions: staminaPotions}
}
