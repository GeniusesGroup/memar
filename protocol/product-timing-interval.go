/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductTimingInterval indicate the domain record data fields.
// e.g. flight duration, doctor visit, carwash, ...
type ProductTimingInterval interface {
	ProductID() ProductUUID      //
	Minimum() protocol.Duration  // Minimum time duration for this service
	Expected() protocol.Duration // Expected time duration for this service
	Maximum() protocol.Duration  // Maximum time duration for this service
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type ProductTimingInterval_StorageServices interface {
	Save(pt ProductTimingInterval) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pt ProductTimingInterval, nv protocol.NumberOfVersion, err protocol.Error)
}
