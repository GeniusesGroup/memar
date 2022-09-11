/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductDuration indicate the domain record data fields.
type ProductDuration interface {
	ProductID() [16]byte         // product domain
	Duration() protocol.Duration // from first use
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type ProductDuration_StorageServices interface {
	Save(pm ProductDuration) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pm ProductDuration, nv protocol.NumberOfVersion, err protocol.Error)
}
