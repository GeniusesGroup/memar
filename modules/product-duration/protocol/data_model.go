/* For license and copyright information please see the LEGAL file in the code repository */

package pdp

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID      //
	Epoch() ProductDuration_Epoch   //
	Duration() protocol.Duration    // from first use
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type ProductDuration_Epoch uint8

const (
	ProductDuration_Epoch_Unset ProductDuration_Epoch = iota
	ProductDuration_Epoch_FirstUse
	ProductDuration_Epoch_PurchaseTime
)
