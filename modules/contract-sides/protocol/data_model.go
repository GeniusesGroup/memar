/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
	cp "org/modules/contract/protocol"
)

type ContractSides interface {
	ContractID() cp.ContractUUID    //
	SideType() ContractSides_ST     //
	UserID() up.UserUUID            //Can be any user type e.g. staff
	UserSignature() []byte          //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type ContractSides_ST uint8

const (
	ContractSides_ST_Unset ContractSides_ST = iota
	ContractSides_ST_First
	ContractSides_ST_Second
	ContractSides_ST_Third
	ContractSides_ST_Witness
	ContractSides_ST_Arbitrator
	ContractSides_ST_Expert
)
