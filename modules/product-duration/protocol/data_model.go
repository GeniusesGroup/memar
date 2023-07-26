/* For license and copyright information please see the LEGAL file in the code repository */

package pdp

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	Epoch() ProductDuration_Epoch
	Duration() protocol.Duration // from first use

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

type ProductDuration_Epoch uint8

const (
	ProductDuration_Epoch_Unset ProductDuration_Epoch = iota
	ProductDuration_Epoch_FirstUse
	ProductDuration_Epoch_PurchaseTime
)
