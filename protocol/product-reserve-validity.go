/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductReserveValidity indicate the domain record data fields.
type ProductReserveValidity interface {
	ProductID() [16]byte         // product domain
	Duration() protocol.Duration // from add to invoice time
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type ProductReserveValidity_StorageServices interface {
	Save(prv ProductReserveValidity) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (prv ProductReserveValidity, nv protocol.NumberOfVersion, err protocol.Error)
}
