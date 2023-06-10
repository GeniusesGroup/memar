/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ContractTemplateStatus interface {
	ContractTemplateID() ContractTemplateUUID //
	Status() ContractTemplate_Status          //
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type ContractTemplateStatus_StorageServices interface {
	Save(cts ContractTemplateStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractTemplateID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractTemplateID [16]byte, vo protocol.VersionOffset) (cts ContractTemplateStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status Content_Status, offset, limit uint64) (contractTemplateIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type ContractTemplate_Status Quiddity_Status

const (
	ContractTemplate_Status_Draft = ContractTemplate_Status(Quiddity_Status_FreeFlag << iota)
)
