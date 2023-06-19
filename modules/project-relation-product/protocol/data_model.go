/* For license and copyright information please see the LEGAL file in the code repository */

package prpp

import (
	"libgo/protocol"

	prp "org/modules/product/protocol"
	pp "org/modules/project/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID  //
	ProductID() prp.ProductUUID //
	Status() Status
	// TODO::: type or label??
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
