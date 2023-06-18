/* For license and copyright information please see the LEGAL file in the code repository */

package pcp

import (
	"libgo/protocol"

	cp "org/modules/content/protocol"
	pp "org/modules/product/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID      //
	ContentID() cp.ContentUUID      //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
