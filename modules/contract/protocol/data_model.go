/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"libgo/protocol"

	ctp "org/modules/contract-template/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ContractID() ContractUUID                     //
	ContractTemplateID() ctp.ContractTemplateUUID //
	ContractTemplateVersion() uint64              // VersionOffset
	Data() map[Type]string                        //
	SaveTime() protocol.Time                      //
	RequestID() urp.UserRequestUUID               //
}

type Type uint32

const (
	Type_Unset Type = iota

	Type_FirstSide
	Type_SecondSide
	Type_ThirdSide
	Type_Witness
	Type_Arbitrator
	Type_Expert

	Type_Mass
	Type_Density

	Type_WeeklyRent
	Type_MonthlyRent

	Type_DueTo
)

// Service: fulfill the obligation
