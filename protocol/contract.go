/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type Contract interface {
	ContractID() [16]byte              // contract domain
	ContractTemplateID() [16]byte      // contract-template domain
	ContractTemplateVersion() uint64   // VersionOffset
	Data() map[Contract_KeyType]string //
	Time() protocol.Time               // save time
	RequestID() UserRequestUUID        // user-request domain
}

type Contract_StorageServices interface {
	Save(c Contract) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractID [16]byte, vo protocol.VersionOffset) (c Contract, nv protocol.NumberOfVersion, err protocol.Error)

	FindByContractTemplate(contractTemplateID [16]byte, offset, limit uint64) (contractIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	FindByData(data string, offset, limit uint64) (contractIDs [16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type Contract_KeyType uint32

const (
	Contract_KeyType_Unset Contract_KeyType = iota

	Contract_KeyType_FirstSide
	Contract_KeyType_SecondSide
	Contract_KeyType_ThirdSide
	Contract_KeyType_Witness
	Contract_KeyType_Arbitrator
	Contract_KeyType_Expert

	Contract_KeyType_Mass
	Contract_KeyType_Density

	Contract_KeyType_WeeklyRent
	Contract_KeyType_MonthlyRent

	Contract_KeyType_DueTo
)

// Service: fulfill the obligation
