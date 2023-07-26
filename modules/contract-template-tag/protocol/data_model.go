/* For license and copyright information please see the LEGAL file in the code repository */

package cttp

import (
	"memar/protocol"

	ctp "org/modules/contract-template/protocol"
)

// DataModel indicate the domain record data fields.
// Tag is any text with hashtag in the contract template text, can't use by old fashion way to assign by users.
type DataModel interface {
	ContractTemplateID() ctp.ContractTemplateUUID
	Tag() string
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
