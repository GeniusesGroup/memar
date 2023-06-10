/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductArea indicate the domain record data fields.
// ProductArea is proper or appropriate location indicate specific area not specific location e.g. Taxi, ...
type ProductArea interface {
	ProductID() ProductUUID //
	EstateID() EstateUUID   //
	Status() ProductArea_Status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductArea_StorageServices interface {
	Save(dm ProductArea) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, estateID EstateUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, estateID EstateUUID, vo protocol.VersionOffset) (dm ProductArea, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_EstateID(estateID EstateUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_EstateIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (estateIDs []EstateUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductArea_Status Quiddity_Status
